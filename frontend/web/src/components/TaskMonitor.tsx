'use client';

import { useState } from 'react';
import { RefreshCw, Clock, CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Task } from '@/types';

interface TaskMonitorProps {
  tasks: Task[];
  onRefresh: () => void;
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'pending':
      return <Clock className="w-4 h-4 text-yellow-500" />;
    case 'processing':
      return <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />;
    case 'completed':
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    case 'failed':
      return <XCircle className="w-4 h-4 text-red-500" />;
    case 'cancelled':
      return <AlertCircle className="w-4 h-4 text-gray-500" />;
    default:
      return <Clock className="w-4 h-4 text-gray-500" />;
  }
};

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'processing':
      return 'bg-blue-100 text-blue-800';
    case 'completed':
      return 'bg-green-100 text-green-800';
    case 'failed':
      return 'bg-red-100 text-red-800';
    case 'cancelled':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};

export default function TaskMonitor({ tasks, onRefresh }: TaskMonitorProps) {
  const [expandedTask, setExpandedTask] = useState<number | null>(null);

  const toggleExpanded = (taskId: number) => {
    setExpandedTask(expandedTask === taskId ? null : taskId);
  };

  const handleCancelTask = async (taskId: number) => {
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${API_BASE_URL}/task/${taskId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        onRefresh();
      } else {
        console.error('Failed to cancel task');
      }
    } catch (error) {
      console.error('Error cancelling task:', error);
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks found. Submit a command to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">
          Recent Tasks ({tasks.length})
        </h3>
        <button
          onClick={onRefresh}
          className="flex items-center space-x-2 px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Refresh</span>
        </button>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <div
            key={task.task_id}
            className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
          >
            {/* Task Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {getStatusIcon(task.status)}
                <div>
                  <h4 className="font-medium text-gray-900">{task.title}</h4>
                  <p className="text-sm text-gray-500">
                    Created: {formatDate(task.created_at)}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                    task.status
                  )}`}
                >
                  {task.status}
                </span>
                {task.status === 'pending' && (
                  <button
                    onClick={() => handleCancelTask(task.task_id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Cancel
                  </button>
                )}
                <button
                  onClick={() => toggleExpanded(task.task_id)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  {expandedTask === task.task_id ? '▼' : '▶'}
                </button>
              </div>
            </div>

            {/* Expanded Details */}
            {expandedTask === task.task_id && (
              <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Started:</span>
                    <p className="text-gray-600">{formatDate(task.started_at)}</p>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Completed:</span>
                    <p className="text-gray-600">{formatDate(task.completed_at)}</p>
                  </div>
                </div>

                {task.error_message && (
                  <div>
                    <span className="font-medium text-gray-700">Error:</span>
                    <p className="text-red-600 text-sm mt-1">{task.error_message}</p>
                  </div>
                )}

                {task.result && (
                  <div>
                    <span className="font-medium text-gray-700">Result:</span>
                    <pre className="text-sm text-gray-600 mt-1 bg-gray-100 p-2 rounded overflow-x-auto">
                      {JSON.stringify(task.result, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}