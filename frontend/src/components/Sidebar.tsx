import React from 'react';
import {
  LayoutDashboard,
  MailSearch,
  History,
  Globe,
  FileText,
  Settings,
  HelpCircle,
  Shield,
  Activity,
} from 'lucide-react';

export type NavTab = 'dashboard' | 'analyze' | 'history' | 'threat-intel' | 'reports' | 'settings' | 'help';

interface SidebarProps {
  activeTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  stats?: { total: number; phishing: number; suspicious: number; avg_score: number };
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onSelectTab }) => {
  const navItems = [
    { id: 'dashboard' as NavTab, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analyze' as NavTab, label: 'Analyze Email', icon: MailSearch },
    { id: 'history' as NavTab, label: 'History', icon: History },
    { id: 'threat-intel' as NavTab, label: 'Threat Intel', icon: Globe },
    { id: 'reports' as NavTab, label: 'Reports', icon: FileText },
    { id: 'settings' as NavTab, label: 'Settings', icon: Settings },
    { id: 'help' as NavTab, label: 'Help', icon: HelpCircle },
  ];

  return (
    <aside className="w-64 bg-[#0B101D] border-r border-[#1E2D4A]/60 flex flex-col justify-between p-4 shrink-0 min-h-screen">
      {/* Brand Header */}
      <div>
        <div className="flex items-center gap-3 px-2 py-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyber-cyan/20 to-cyber-blue/30 border border-cyber-cyan/40 flex items-center justify-center text-cyber-cyan shadow-cyan-glow">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-wide flex items-center gap-1.5">
              E-Unthreat
            </h1>
            <p className="text-xs text-cyber-muted font-medium">Email Threat Intelligence</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`w-full flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-600/20 text-white border border-blue-500/40 shadow-blue-glow font-semibold'
                    : 'text-cyber-text-secondary hover:text-white hover:bg-white/[0.04]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyber-cyan' : 'text-cyber-muted'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom System Status Widget */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-xl p-3.5 mt-6">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs font-semibold text-cyber-text-secondary flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-cyber-cyan" />
            System Status
          </span>
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-cyber-success">
            <span className="w-1.5 h-1.5 rounded-full bg-cyber-success animate-ping inline-block" />
            Operational
          </span>
        </div>
        <p className="text-[11px] text-cyber-muted mb-2">All systems running</p>

        {/* Mini Sparkline Graph */}
        <div className="h-7 w-full overflow-hidden">
          <svg className="w-full h-full" viewBox="0 0 100 25" fill="none" preserveAspectRatio="none">
            <path
              d="M0 18 Q 15 5, 30 14 T 60 8 T 85 16 T 100 6"
              stroke="#10B981"
              strokeWidth="2"
              strokeLinecap="round"
              fill="none"
            />
            <path
              d="M0 18 Q 15 5, 30 14 T 60 8 T 85 16 T 100 6 L 100 25 L 0 25 Z"
              fill="url(#sparkline-grad)"
              opacity="0.25"
            />
            <defs>
              <linearGradient id="sparkline-grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10B981" />
                <stop offset="100%" stopColor="#10B981" stopOpacity="0" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </aside>
  );
};
