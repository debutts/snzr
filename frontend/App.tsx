import { LogtoConfig, LogtoProvider } from '@logto/rn';
import React from 'react';
import "./global.css";
import { ProtectedRoute } from './views/protectedRoute';

const config: LogtoConfig = {
  endpoint: process.env.LOGTO_ENDPOINT,
  appId: process.env.LOGTO_APP_ID,
};

export default function App() {
  return (
    <LogtoProvider config={config}>
      <ProtectedRoute/>
    </LogtoProvider>
  );
}
