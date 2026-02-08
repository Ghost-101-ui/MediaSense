"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MediaInput from "@/components/MediaInput";
import PreviewCard from "@/components/PreviewCard";
import FloatingLines from "@/components/FloatingLines";
import ShinyText from "@/components/ShinyText";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [mediaData, setMediaData] = useState(null);
  const [error, setError] = useState("");

  console.log("Home render: url=", url, "loading=", loading);

  const handleFetch = async () => {
    if (!url) return;
    setLoading(true);
    setError("");
    setMediaData(null);

    try {
      // Use environment variable for API URL, fallback to localhost for development
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

      const res = await fetch(`${API_URL}/analyze/?url=${encodeURIComponent(url)}`);
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to fetch media");
      }
      const data = await res.json();
      setMediaData(data);

    } catch (err: any) {
      setError(err.message || "Failed to fetch media. Please check the link.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-neutral-950 text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Animated FloatingLines Background */}
      <FloatingLines
        linesGradient={['#4c1d95', '#1e3a8a', '#7f1d1d']}
        enabledWaves={['top', 'middle', 'bottom']}
        lineCount={8}
        lineDistance={3}
        bendRadius={3}
        bendStrength={-0.8}
        interactive={true}
        parallax={true}
        animationSpeed={0.5}
        mixBlendMode="screen"
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center w-full max-w-3xl z-10"
      >
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
          MediaSense
          {/* <ShinyText
            text="MediaSense"
            speed={3}
            delay={1}
            color="#7c3aed"
            shineColor="#c4b5fd"
            spread={90}
            direction="left"
          /> */}
        </h1>
        <p className="text-lg md:text-xl text-neutral-400 mb-12">
          Universal Media Downloader. Secure. Fast. Premium.
        </p>

        <div className="w-full max-w-xl mx-auto space-y-8">
          <MediaInput
            value={url}
            onChange={setUrl}
            onSubmit={handleFetch}
            loading={loading}
          />

          <AnimatePresence mode="wait">
            {error && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="text-red-400 flex items-center justify-center gap-2 bg-red-950/30 p-3 rounded-lg border border-red-900/50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" x2="12" y1="8" y2="12" />
                  <line x1="12" x2="12.01" y1="16" y2="16" />
                </svg>
                <span>{error}</span>
              </motion.div>
            )}

            {mediaData && (
              <PreviewCard data={mediaData} url={url} />
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      <footer className="absolute bottom-6 text-neutral-600 text-sm flex gap-4">
        <p>© 2026 MediaSense. Secure & Ad-Friendly.</p>
        <div className="flex gap-4">
          <a href="/legal/privacy" className="hover:text-neutral-400 transition-colors">Privacy Policy</a>
          <a href="/legal/tos" className="hover:text-neutral-400 transition-colors">Terms of Service</a>
        </div>
      </footer>
    </main>
  );
}
