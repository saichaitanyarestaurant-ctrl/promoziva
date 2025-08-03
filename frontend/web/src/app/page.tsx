'use client';

import { useState, useEffect } from 'react';
import CommandInput from '@/components/CommandInput';
import TaskMonitor from '@/components/TaskMonitor';
import ServiceStatus from '@/components/ServiceStatus';
import QueueStatus from '@/components/QueueStatus';
import { Task, QueueStatus as QueueStatusType, ServiceHealth } from '@/types';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [queueStatus, setQueueStatus] = useState<QueueStatusType | null>(null);
  const [serviceHealth, setServiceHealth] = useState<ServiceHealth | null>(null);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  useEffect(() => {
    fetchInitialData();
    const interval = setInterval(fetchInitialData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchInitialData = async () => {
    try {
      const [tasksRes, queueRes, healthRes] = await Promise.all([
        fetch(`${API_BASE_URL}/tasks?limit=10`),
        fetch(`${API_BASE_URL}/queue/status`),
        fetch(`${API_BASE_URL}/services/health`)
      ]);

      if (tasksRes.ok) {
        const tasksData = await tasksRes.json();
        setTasks(tasksData);
      }

      if (queueRes.ok) {
        const queueData = await queueRes.json();
        setQueueStatus(queueData);
      }

      if (healthRes.ok) {
        const healthData = await healthRes.json();
        setServiceHealth(healthData);
      }
    } catch (error) {
      console.error('Error fetching initial data:', error);
    }
  };

  const handleCommandSubmit = async (command: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          command,
          user_id: 1, // Default user ID
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Command submitted:', result);
        // Refresh data after command submission
        await fetchInitialData();
      } else {
        const error = await response.json();
        console.error('Error submitting command:', error);
      }
    } catch (error) {
      console.error('Error submitting command:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">AI Orchestrator Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Manage your AI tasks and monitor service status
          </p>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Command Input and Task Monitor */}
          <div className="lg:col-span-2 space-y-8">
            {/* Command Input */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Command Interface
              </h2>
              <CommandInput onSubmit={handleCommandSubmit} loading={loading} />
            </div>

            {/* Task Monitor */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Task Monitor
              </h2>
              <TaskMonitor tasks={tasks} onRefresh={fetchInitialData} />
            </div>
          </div>

          {/* Right Column - Status Panels */}
          <div className="space-y-8">
            {/* Queue Status */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Queue Status
              </h2>
              <QueueStatus status={queueStatus} />
            </div>

            {/* Service Health */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Service Health
              </h2>
              <ServiceStatus health={serviceHealth} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
