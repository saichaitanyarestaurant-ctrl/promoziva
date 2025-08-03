'use client';

import { QueueStatus as QueueStatusType } from '@/types';
import { Clock, Play, CheckCircle, XCircle, Users } from 'lucide-react';

interface QueueStatusProps {
  status: QueueStatusType | null;
}

export default function QueueStatus({ status }: QueueStatusProps) {
  if (!status) {
    return (
      <div className="text-center py-4">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3 mx-auto"></div>
        </div>
      </div>
    );
  }

  const totalTasks = status.total_pending + status.total_processing + status.total_completed + status.total_failed;
  const completionRate = totalTasks > 0 ? ((status.total_completed + status.total_failed) / totalTasks * 100).toFixed(1) : '0';

  return (
    <div className="space-y-4">
      {/* Queue Overview */}
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-center mb-2">
            <Clock className="w-5 h-5 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-blue-900">{status.queue_size}</div>
          <div className="text-sm text-blue-700">In Queue</div>
        </div>
        
        <div className="text-center p-3 bg-green-50 rounded-lg">
          <div className="flex items-center justify-center mb-2">
            <Play className="w-5 h-5 text-green-600" />
          </div>
          <div className="text-2xl font-bold text-green-900">{status.active_tasks}</div>
          <div className="text-sm text-green-700">Active</div>
        </div>
      </div>

      {/* Task Status Breakdown */}
      <div className="space-y-3">
        <div className="flex items-center justify-between p-2 bg-yellow-50 rounded">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-yellow-600" />
            <span className="text-sm font-medium text-yellow-800">Pending</span>
          </div>
          <span className="text-sm font-bold text-yellow-900">{status.total_pending}</span>
        </div>

        <div className="flex items-center justify-between p-2 bg-blue-50 rounded">
          <div className="flex items-center space-x-2">
            <Play className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-800">Processing</span>
          </div>
          <span className="text-sm font-bold text-blue-900">{status.total_processing}</span>
        </div>

        <div className="flex items-center justify-between p-2 bg-green-50 rounded">
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <span className="text-sm font-medium text-green-800">Completed</span>
          </div>
          <span className="text-sm font-bold text-green-900">{status.total_completed}</span>
        </div>

        <div className="flex items-center justify-between p-2 bg-red-50 rounded">
          <div className="flex items-center space-x-2">
            <XCircle className="w-4 h-4 text-red-600" />
            <span className="text-sm font-medium text-red-800">Failed</span>
          </div>
          <span className="text-sm font-bold text-red-900">{status.total_failed}</span>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="pt-4 border-t border-gray-200">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Max Concurrent Tasks:</span>
            <span className="font-medium text-gray-900">{status.max_concurrent_tasks}</span>
          </div>
          
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Completion Rate:</span>
            <span className="font-medium text-gray-900">{completionRate}%</span>
          </div>

          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Total Tasks:</span>
            <span className="font-medium text-gray-900">{totalTasks}</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="pt-2">
        <div className="flex items-center space-x-2 mb-2">
          <Users className="w-4 h-4 text-gray-400" />
          <span className="text-sm text-gray-600">Task Progress</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ 
              width: `${completionRate}%`,
              background: `linear-gradient(90deg, 
                ${status.total_completed > 0 ? '#10B981' : '#3B82F6'} 0%, 
                ${status.total_failed > 0 ? '#EF4444' : '#3B82F6'} 100%)`
            }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>0</span>
          <span>{totalTasks}</span>
        </div>
      </div>
    </div>
  );
}