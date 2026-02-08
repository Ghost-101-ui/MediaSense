"use client";

import { useState } from "react";
import { motion } from "framer-motion";


interface MediaInputProps {
    value: string;
    onChange: (val: string) => void;
    onSubmit: () => void;
    loading: boolean;
}

export default function MediaInput({ value, onChange, onSubmit, loading }: MediaInputProps) {
    console.log("MediaInput render: value=", value, "loading=", loading);
    const [focused, setFocused] = useState(false);

    return (
        <motion.div
            className={`relative w-full rounded-2xl p-[1px] transition-all duration-300 ${focused ? 'bg-gradient-to-br from-white/30 to-white/10 shadow-2xl shadow-blue-500/20' : 'bg-gradient-to-br from-white/20 to-white/5'}`}
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2 }}
        >
            <div className="relative flex items-center bg-white/[0.02] backdrop-blur-2xl rounded-2xl overflow-hidden border border-white/20 shadow-xl shadow-black/20">
                {/* Glass highlight effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent pointer-events-none" />

                <div className="pl-4 text-neutral-400">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="11" cy="11" r="8" />
                        <path d="m21 21-4.3-4.3" />
                    </svg>
                </div>
                <input
                    type="text"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onFocus={() => setFocused(true)}
                    onBlur={() => setFocused(false)}
                    onKeyDown={(e) => e.key === "Enter" && onSubmit()}
                    placeholder="Paste URL from YouTube, Pinterest, Instagram, X..."
                    className="flex-1 min-w-0 bg-transparent border-none text-white p-4 focus:ring-0 outline-none placeholder-neutral-500"
                    style={{ color: 'white', WebkitTextFillColor: 'white' }}
                    disabled={loading}
                />
                <div className="pr-2">
                    <button
                        onClick={onSubmit}
                        disabled={loading || !value}
                        className={`px-4 py-2 rounded-xl transition-all duration-300 ${loading || !value ? 'opacity-50 bg-white/10 text-neutral-500' : 'bg-white text-black hover:bg-neutral-200 cursor-pointer'}`}
                    >
                        {loading ? (
                            <svg className="animate-spin" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                            </svg>
                        ) : "Fetch"}
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
