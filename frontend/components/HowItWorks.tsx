"use client";

import { motion } from "framer-motion";
import { Copy, Link, Download } from "lucide-react";

export default function HowItWorks() {
    const steps = [
        {
            title: "1. Copy Link",
            icon: <Copy className="w-6 h-6" />,
            description: "Copy the video URL from Pinterest or X (Twitter).",
        },
        {
            title: "2. Paste Here",
            icon: <Link className="w-6 h-6" />,
            description: "Paste the link into the MediaSense input box above.",
        },
        {
            title: "3. Download",
            icon: <Download className="w-6 h-6" />,
            description: "Select your preferred format and download instantly.",
        },
    ];

    return (
        <section className="w-full max-w-4xl mx-auto mt-20 mb-10 px-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="text-center mb-10"
            >
                <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-4">
                    How It Works
                </h2>
                <p className="text-neutral-400">
                    Download content from your favorite platforms in 3 simple steps.
                </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8">
                {/* Pinterest Card */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-3xl p-6 hover:border-red-500/30 transition-colors group"
                >
                    <div className="flex items-center gap-3 mb-6">
                        {/* Simple Pinterest-like circle */}
                        <div className="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-lg">
                            P
                        </div>
                        <h3 className="text-xl font-bold text-neutral-200">Pinterest</h3>
                    </div>

                    <div className="space-y-4">
                        {steps.map((step, idx) => (
                            <div key={idx} className="flex items-start gap-3 text-sm text-neutral-400">
                                <div className="bg-neutral-800 p-2 rounded-lg text-red-400 group-hover:text-red-300 transition-colors">
                                    {step.icon}
                                </div>
                                <div>
                                    <p className="font-semibold text-neutral-200">{step.title}</p>
                                    <p className="text-xs mt-1">{step.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* X (Twitter) Card */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                    className="bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-3xl p-6 hover:border-blue-500/30 transition-colors group"
                >
                    <div className="flex items-center gap-3 mb-6">
                        {/* X Logo simulation */}
                        <div className="w-10 h-10 rounded-full bg-black border border-neutral-700 flex items-center justify-center text-white font-bold text-lg">
                            X
                        </div>
                        <h3 className="text-xl font-bold text-neutral-200">X (Twitter)</h3>
                    </div>

                    <div className="space-y-4">
                        {steps.map((step, idx) => (
                            <div key={idx} className="flex items-start gap-3 text-sm text-neutral-400">
                                <div className="bg-neutral-800 p-2 rounded-lg text-blue-400 group-hover:text-blue-300 transition-colors">
                                    {step.icon}
                                </div>
                                <div>
                                    <p className="font-semibold text-neutral-200">{step.title}</p>
                                    <p className="text-xs mt-1">{step.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
