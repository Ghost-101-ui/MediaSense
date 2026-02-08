"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Download, Clock, MonitorPlay, Music, CheckCircle, AlertOctagon } from "lucide-react";

interface Format {
    resolution: string;
    ext: string;
    size: string;
    format_id: string;
    type: string;
}

interface MediaData {
    title: string;
    thumbnail: string;
    duration: string;
    platform: string;
    formats: Format[];
}

interface PreviewCardProps {
    data: MediaData;
    url: string;
}

const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
};

export default function PreviewCard({ data, url }: PreviewCardProps) {
    const [downloadState, setDownloadState] = useState<{
        status: 'idle' | 'starting' | 'downloading' | 'completed' | 'error',
        progress: number,
        taskId?: string,
        error?: string,
        formatId?: string
    }>({ status: 'idle', progress: 0 });

    const API_URL = "http://localhost:8000/api/v1";

    const handleDownload = async (formatId: string) => {
        setDownloadState({ status: 'starting', progress: 0, formatId });

        try {
            const res = await fetch(`${API_URL}/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, format_id: formatId })
            });

            if (!res.ok) throw new Error("Failed to start download");

            const { task_id } = await res.json();
            setDownloadState(prev => ({ ...prev, status: 'downloading', taskId: task_id }));

            const interval = setInterval(async () => {
                try {
                    const statusRes = await fetch(`${API_URL}/download/status/${task_id}`);
                    const statusData = await statusRes.json();

                    if (statusData.status === 'completed') {
                        clearInterval(interval);
                        setDownloadState(prev => ({ ...prev, status: 'completed', progress: 100 }));
                        window.location.href = `${API_URL}/download/file/${task_id}`;
                    } else if (statusData.status === 'failed') {
                        clearInterval(interval);
                        setDownloadState(prev => ({ ...prev, status: 'error', error: statusData.error || "Download failed" }));
                    } else {
                        setDownloadState(prev => ({ ...prev, progress: statusData.progress || 0 }));
                    }
                } catch (e) {
                    clearInterval(interval);
                    setDownloadState(prev => ({ ...prev, status: 'error', error: "Connection lost" }));
                }
            }, 1000);

        } catch (e: any) {
            setDownloadState(prev => ({ ...prev, status: 'error', error: e.message }));
        }
    };

    return (
        <motion.div
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={{
                visible: { transition: { staggerChildren: 0.1 } }
            }}
            className="w-full bg-neutral-900/80 backdrop-blur-md rounded-3xl overflow-hidden border border-neutral-800 shadow-2xl mt-8"
        >
            <div className="grid md:grid-cols-2 gap-6 p-6">
                <motion.div variants={itemVariants} className="relative aspect-video rounded-2xl overflow-hidden bg-black/50 group">
                    <img
                        src={data.thumbnail}
                        alt={data.title}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    <div className="absolute bottom-2 right-2 bg-black/70 backdrop-blur text-xs px-2 py-1 rounded-md flex items-center gap-1 font-mono">
                        <Clock size={12} /> {data.duration}
                    </div>
                </motion.div>

                <motion.div variants={itemVariants} className="flex flex-col gap-4">
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-bold uppercase tracking-wider text-blue-400 bg-blue-950/30 px-2 py-1 rounded-md border border-blue-900/50">
                                {data.platform}
                            </span>
                        </div>
                        <h3 className="text-xl font-bold line-clamp-2 leading-tight text-neutral-100">
                            {data.title}
                        </h3>
                    </div>

                    <AnimatePresence mode="wait">
                        {downloadState.status !== 'idle' && downloadState.status !== 'error' ? (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                className="bg-neutral-800 rounded-xl p-4 border border-neutral-700 space-y-2"
                            >
                                <div className="flex justify-between text-sm text-neutral-300">
                                    <span>{downloadState.status === 'starting' ? 'Preparing...' :
                                        downloadState.status === 'completed' ? 'Download Ready' :
                                            'Downloading...'}</span>
                                    <span>{Math.round(downloadState.progress)}%</span>
                                </div>
                                <div className="h-2 bg-neutral-700 rounded-full overflow-hidden">
                                    <motion.div
                                        className="h-full bg-blue-500"
                                        initial={{ width: 0 }}
                                        animate={{ width: `${downloadState.progress}%` }}
                                        transition={{ duration: 0.5 }}
                                    />
                                </div>
                                {downloadState.status === 'completed' && (
                                    <div className="flex items-center gap-2 text-green-400 text-sm mt-2">
                                        <CheckCircle size={16} /> <span>File downloaded automatically</span>
                                    </div>
                                )}
                            </motion.div>
                        ) : (
                            <div className="flex-1 overflow-y-auto max-h-[250px] pr-2 space-y-2 custom-scrollbar">
                                {downloadState.status === 'error' && (
                                    <div className="text-red-400 text-sm bg-red-950/30 p-2 rounded flex items-center gap-2 mb-2">
                                        <AlertOctagon size={16} /> {downloadState.error}
                                        <button onClick={() => setDownloadState({ status: 'idle', progress: 0 })} className="ml-auto underline">Dismiss</button>
                                    </div>
                                )}

                                {data.formats.map((fmt, idx) => (
                                    <motion.div
                                        key={idx}
                                        variants={itemVariants}
                                        className="flex items-center justify-between p-3 rounded-xl bg-neutral-800/50 hover:bg-neutral-800 border border-neutral-700/50 hover:border-neutral-600 transition-colors group cursor-pointer"
                                        onClick={() => handleDownload(fmt.format_id)}
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className={`p-2 rounded-lg ${fmt.ext === 'mp3' ? 'bg-purple-500/10 text-purple-400' : 'bg-blue-500/10 text-blue-400'}`}>
                                                {fmt.ext === 'mp3' ? <Music size={18} /> : <MonitorPlay size={18} />}
                                            </div>
                                            <div>
                                                <div className="font-medium text-sm text-neutral-200">{fmt.resolution}</div>
                                                <div className="text-xs text-neutral-500 uppercase">{fmt.ext} • {fmt.size}</div>
                                            </div>
                                        </div>
                                        <div className="p-2 rounded-lg bg-neutral-700 group-hover:bg-white group-hover:text-black transition-colors">
                                            <Download size={18} />
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </motion.div>
    );
}
