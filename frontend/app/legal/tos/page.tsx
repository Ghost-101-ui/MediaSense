export default function TermsOfService() {
    return (
        <div className="min-h-screen bg-neutral-950 text-white p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">Terms of Service</h1>
            <p className="mb-4">Last updated: February 2026</p>

            <h2 className="text-xl font-bold mt-6 mb-2">1. Acceptance of Terms</h2>
            <p className="mb-4">By accessing MediaSense, you agree to these Terms. If you disagree, do not use the Service.</p>

            <h2 className="text-xl font-bold mt-6 mb-2">2. Use of Service</h2>
            <ul className="list-disc ml-6 mb-4 text-neutral-400">
                <li>You agree to use this Service only for personal, non-commercial use.</li>
                <li>You must respect the intellectual property rights of content creators.</li>
                <li>You must not download copyrighted material without permission.</li>
                <li>We reserve the right to block any user or IP address for abuse.</li>
            </ul>

            <h2 className="text-xl font-bold mt-6 mb-2">3. Disclaimer</h2>
            <p className="mb-4">The Service is provided "AS IS". We make no warranties regarding availability or accuracy.</p>

            <h2 className="text-xl font-bold mt-6 mb-2">4. Limitation of Liability</h2>
            <p className="mb-4">We shall not be liable for any indirect, incidental, or consequential damages resulting from your use of the Service.</p>
        </div>
    );
}
