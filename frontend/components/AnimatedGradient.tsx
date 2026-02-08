"use client";

export default function AnimatedGradient() {
    return (
        <div className="absolute inset-0 w-full h-full">
            {/* Animated gradient orbs */}
            <div
                className="absolute w-[600px] h-[600px] rounded-full opacity-30 blur-3xl animate-float"
                style={{
                    background: 'radial-gradient(circle, rgba(147, 51, 234, 0.4) 0%, transparent 70%)',
                    top: '-10%',
                    left: '-10%',
                    animation: 'float 20s ease-in-out infinite',
                }}
            />
            <div
                className="absolute w-[500px] h-[500px] rounded-full opacity-30 blur-3xl"
                style={{
                    background: 'radial-gradient(circle, rgba(59, 130, 246, 0.4) 0%, transparent 70%)',
                    bottom: '-10%',
                    right: '-10%',
                    animation: 'float 25s ease-in-out infinite reverse',
                }}
            />
            <div
                className="absolute w-[400px] h-[400px] rounded-full opacity-25 blur-3xl"
                style={{
                    background: 'radial-gradient(circle, rgba(236, 72, 153, 0.3) 0%, transparent 70%)',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    animation: 'float 30s ease-in-out infinite',
                }}
            />
        </div>
    );
}
