export default function PrivacyPolicy() {
    return (
        <div className="min-h-screen bg-neutral-950 text-white p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>
            <p className="mb-4">Last updated: February 2026</p>

            <p className="mb-4">
                MediaSense ("we", "us", "our") respects your privacy. This Privacy Policy explains how we collect and use your information.
            </p>

            <h2 className="text-xl font-bold mt-6 mb-2">1. Information We Collect</h2>
            <p className="mb-2">We do not require account registration. We may collect:</p>
            <ul className="list-disc ml-6 mb-4 text-neutral-400">
                <li>Usage Data (e.g., URLs processed, browser type) for analytics and debugging.</li>
                <li>IP Addresses (temporarily stored for rate limiting and abuse prevention).</li>
            </ul>

            <h2 className="text-xl font-bold mt-6 mb-2">2. How We Use Information</h2>
            <p className="mb-4">To provide and maintain our Service, monitor usage, and detect technical issues.</p>

            <h2 className="text-xl font-bold mt-6 mb-2">3. Media Content</h2>
            <p className="mb-4">We do not host files long-term. Extracted media is temporarily stored for download and automatically deleted shortly after.</p>

            <h2 className="text-xl font-bold mt-6 mb-2">4. Third-Party Links</h2>
            <p className="mb-4">Our Service allows downloading from third-party platforms. We are not responsible for their content or privacy practices.</p>
        </div>
    );
}
