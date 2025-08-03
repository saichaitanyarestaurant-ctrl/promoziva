'use client';

import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface CommandInputProps {
  onSubmit: (command: string) => void;
  loading: boolean;
}

const exampleCommands = [
  "Go to google.com and search for 'AI automation'",
  "Create a Google Sheet with sales data for Q1 2024",
  "Make a phone call to +1234567890 and leave a message",
  "Transcribe the video at https://example.com/video.mp4",
  "Create a Make.com workflow to sync data between systems",
  "Design a presentation in Canva about AI trends"
];

export default function CommandInput({ onSubmit, loading }: CommandInputProps) {
  const [command, setCommand] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim() && !loading) {
      onSubmit(command.trim());
      setCommand('');
    }
  };

  const handleExampleClick = (example: string) => {
    setCommand(example);
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Enter your command here... (e.g., 'Go to google.com and search for AI automation')"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={3}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!command.trim() || loading}
            className="absolute bottom-3 right-3 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>

      {/* Example Commands */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-2">Example Commands:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {exampleCommands.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="text-left p-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded border border-gray-200 hover:border-gray-300 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Status */}
      {loading && (
        <div className="flex items-center space-x-2 text-sm text-blue-600">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span>Processing your command...</span>
        </div>
      )}
    </div>
  );
}