'use client';

import { Wifi, WifiOff, Activity } from 'lucide-react';
import { ServiceHealth } from '@/types';

interface ServiceStatusProps {
  health: ServiceHealth | null;
}

const serviceNames = {
  browser_service: 'Browser Automation',
  document_service: 'Document Management',
  communication_service: 'Communication',
  media_service: 'Media Processing',
  bot_builder_service: 'AI Bot Builder'
};

const serviceDescriptions = {
  browser_service: 'Web automation and interactions',
  document_service: 'Google Docs and Sheets management',
  communication_service: 'Voice calls and messaging',
  media_service: 'Video and audio processing',
  bot_builder_service: 'AI bot creation and deployment'
};

export default function ServiceStatus({ health }: ServiceStatusProps) {
  if (!health) {
    return (
      <div className="text-center py-4">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto"></div>
        </div>
      </div>
    );
  }

  const services = Object.entries(health.services);

  return (
    <div className="space-y-3">
      {services.map(([serviceKey, isHealthy]) => {
        const serviceName = serviceNames[serviceKey as keyof typeof serviceNames] || serviceKey;
        const description = serviceDescriptions[serviceKey as keyof typeof serviceDescriptions] || 'Service';

        return (
          <div
            key={serviceKey}
            className={`flex items-center justify-between p-3 rounded-lg border ${
              isHealthy
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}
          >
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${
                isHealthy ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {isHealthy ? (
                  <Wifi className="w-4 h-4 text-green-600" />
                ) : (
                  <WifiOff className="w-4 h-4 text-red-600" />
                )}
              </div>
              <div>
                <h4 className="font-medium text-gray-900">{serviceName}</h4>
                <p className="text-sm text-gray-500">{description}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                isHealthy ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              <span className={`text-sm font-medium ${
                isHealthy ? 'text-green-700' : 'text-red-700'
              }`}>
                {isHealthy ? 'Healthy' : 'Unhealthy'}
              </span>
            </div>
          </div>
        );
      })}

      {/* Summary */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Overall Status:</span>
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-gray-400" />
            <span className="font-medium text-gray-900">
              {services.filter(([, healthy]) => healthy).length} / {services.length} Healthy
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}