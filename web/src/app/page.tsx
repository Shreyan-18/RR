'use client';

import React, { useState } from 'react';
import cricketData from '@/data/cricket_data.json';
import { 
  Trophy, 
  LayoutGrid, 
  Shield, 
  Gauge, 
  BookOpen, 
  Github, 
  Zap, 
  Target, 
  ChevronRight, 
  X, 
  Sliders, 
  Database, 
  Flame, 
  Users, 
  Crown,
  Crosshair,
  Award,
  Brain,
  CheckCircle,
  Compass
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'leaderboard' | 'quadrants' | 'lineup' | 'simulator' | 'methodology'>('leaderboard');
  const [role, setRole] = useState<'batters' | 'bowlers'>('batters');
  const [selectedPlayer, setSelectedPlayer] = useState<any | null>(null);

  // Simulator states
  const [rrr, setRrr] = useState<number>(11.5);
  const [balls, setBalls] = useState<number>(24);
  const [wickets, setWickets] = useState<number>(5);
  const [stakes, setStakes] = useState<number>(0.85);
  const [isFortress, setIsFortress] = useState<boolean>(true);

  // Compute live pressure
  const rrrNorm = Math.min(1.0, Math.max(0.0, (rrr - 6.0) / 10.0));
  const ballsNorm = Math.min(1.0, Math.max(0.0, (120 - balls) / 96.0));
  const wktsNorm = Math.min(1.0, wickets / 8.0);
  const sMicro = 0.45 * rrrNorm + 0.35 * ballsNorm + 0.20 * wktsNorm;

  const fortressVal = isFortress ? 1.0 : 0.0;
  const cMacro = 0.50 * stakes + 0.35 * 0.85 + 0.15 * fortressVal;

  let pBall = 0.40 * cMacro + 0.60 * sMicro;
  pBall = Math.min(1.0, Math.max(0.1, pBall));
  const pPercent = Math.round(pBall * 100);

  const playersList = role === 'batters' ? cricketData.batters : cricketData.bowlers;

  return (
    <div className="min-h-screen bg-[#050811] text-slate-100 font-sans selection:bg-[#EA1A85] selection:text-white pb-16 relative">
      
      {/* Subtle ambient lighting */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#EA1A85]/10 rounded-full blur-3xl"></div>
        <div className="absolute top-1/3 -right-40 w-96 h-96 bg-[#00F5D4]/8 rounded-full blur-3xl"></div>
      </div>

      {/* HEADER / NAVIGATION (Clean Title without Badges - Request 1) */}
      <header className="sticky top-0 z-50 bg-[#050811]/95 backdrop-blur-xl border-b border-[#1A2A44] shadow-xl shadow-black/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3.5">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-[#EA1A85] via-[#B80E64] to-[#001C58] flex items-center justify-center font-black text-white text-lg shadow-lg shadow-[#EA1A85]/30 border border-[#EA1A85]/40 flex-shrink-0">
              RR
            </div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl sm:text-2xl font-black tracking-tight text-white leading-none">
                SupeRR Selector <span className="bg-gradient-to-r from-[#FF66B2] to-[#EA1A85] bg-clip-text text-transparent font-extrabold">Analytics Hub</span>
              </h1>
            </div>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center space-x-1 bg-[#0B1322]/90 p-1 rounded-xl border border-[#1A2A44] shadow-inner">
            <button
              onClick={() => setActiveTab('leaderboard')}
              className={`px-4 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'leaderboard'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#0F1A2E]'
              }`}
            >
              <Trophy className="w-3.5 h-3.5" /> Leaderboard
            </button>
            <button
              onClick={() => setActiveTab('quadrants')}
              className={`px-4 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'quadrants'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#0F1A2E]'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" /> 4-Quadrant
            </button>
            <button
              onClick={() => setActiveTab('lineup')}
              className={`px-4 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'lineup'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#0F1A2E]'
              }`}
            >
              <Shield className="w-3.5 h-3.5" /> Pressure-Proof XI
            </button>
            <button
              onClick={() => setActiveTab('simulator')}
              className={`px-4 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'simulator'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#0F1A2E]'
              }`}
            >
              <Gauge className="w-3.5 h-3.5" /> Simulator
            </button>
            <button
              onClick={() => setActiveTab('methodology')}
              className={`px-4 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'methodology'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#0F1A2E]'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" /> Methodology
            </button>
          </nav>

          {/* Quick link */}
          <div className="flex items-center space-x-3">
            <a
              href="https://github.com/Shreyan-18/RR.git"
              target="_blank"
              rel="noreferrer"
              className="px-3.5 py-2 rounded-lg bg-[#0F1A2E] hover:bg-[#14233D] text-slate-200 text-xs font-bold border border-[#1A2A44] transition flex items-center gap-1.5 shadow"
            >
              <Github className="w-4 h-4" /> GitHub
            </a>
          </div>
        </div>

        {/* Mobile Navigation Bar */}
        <div className="md:hidden flex overflow-x-auto px-4 py-2 space-x-2 bg-[#0B1322] border-t border-[#1A2A44]">
          {(['leaderboard', 'quadrants', 'lineup', 'simulator', 'methodology'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setActiveTab(t)}
              className={`text-xs whitespace-nowrap px-3 py-1.5 rounded-lg font-bold capitalize ${
                activeTab === t ? 'bg-[#EA1A85] text-white' : 'text-slate-400'
              }`}
            >
              {t === 'lineup' ? 'Pressure XI' : t}
            </button>
          ))}
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 relative z-10">
        
        {/* STATS STRIP */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 backdrop-blur-md rounded-2xl p-4 border border-[#1A2A44] hover:border-[#EA1A85]/40 transition relative overflow-hidden">
            <Database className="w-16 h-16 absolute right-2 -bottom-2 text-[#EA1A85]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">Total Deliveries</p>
            <p className="text-2xl sm:text-3xl font-black font-mono text-white mt-1">200,999</p>
            <span className="text-xs text-[#FF3399] font-semibold mt-1 inline-flex items-center gap-1">
              <CheckCircle className="w-3.5 h-3.5" /> 867 Matches (IPL & T20I)
            </span>
          </div>

          <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 backdrop-blur-md rounded-2xl p-4 border border-[#1A2A44] hover:border-[#00F5D4]/40 transition relative overflow-hidden">
            <Flame className="w-16 h-16 absolute right-2 -bottom-2 text-[#00F5D4]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">High Pressure Split</p>
            <p className="text-2xl sm:text-3xl font-black font-mono text-[#00F5D4] mt-1">60,314</p>
            <span className="text-xs text-slate-300 font-semibold mt-1 inline-block">Top 30% Leverage (P ≥ 0.70)</span>
          </div>

          <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 backdrop-blur-md rounded-2xl p-4 border border-[#1A2A44] hover:border-[#F59E0B]/40 transition relative overflow-hidden">
            <Users className="w-16 h-16 absolute right-2 -bottom-2 text-[#F59E0B]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">Qualified Players</p>
            <p className="text-2xl sm:text-3xl font-black font-mono text-white mt-1">405</p>
            <span className="text-xs text-[#F59E0B] font-semibold mt-1 inline-block">162 Batters • 243 Bowlers</span>
          </div>

          <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 backdrop-blur-md rounded-2xl p-4 border border-[#1A2A44] hover:border-[#EA1A85]/40 transition relative overflow-hidden">
            <Crown className="w-16 h-16 absolute right-2 -bottom-2 text-[#EA1A85]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">#1 Clutch Ranks</p>
            <p className="text-lg sm:text-xl font-black text-white mt-1 truncate">N. Dhir & S. Narine</p>
            <span className="text-xs text-[#FF3399] font-semibold mt-1 inline-block">Scores: 87.7 (Bat) • 76.8 (Bowl)</span>
          </div>
        </section>

        {/* TAB 1: LEADERBOARDS */}
        {activeTab === 'leaderboard' && (
          <section className="space-y-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-[#1A2A44]">
              <div>
                <h2 className="text-2xl font-black text-white flex items-center gap-2">
                  Official Pressure Rankings <span className="bg-gradient-to-r from-[#FF66B2] to-[#EA1A85] bg-clip-text text-transparent text-base font-bold">• Top 10</span>
                </h2>
                <p className="text-sm text-slate-400 mt-0.5">
                  Audited across 867 fixtures, prioritizing boundary conversion (27.5%), post-boundary composure (46.8%), and macro stakes.
                </p>
              </div>

              {/* Batters vs Bowlers Toggle */}
              <div className="flex items-center bg-[#0B1322] p-1 rounded-xl border border-[#1A2A44] shadow-inner">
                <button
                  onClick={() => setRole('batters')}
                  className={`px-5 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider flex items-center gap-1.5 transition ${
                    role === 'batters' ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Zap className="w-4 h-4" /> Batters (10)
                </button>
                <button
                  onClick={() => setRole('bowlers')}
                  className={`px-5 py-2 rounded-lg text-xs uppercase font-extrabold tracking-wider flex items-center gap-1.5 transition ${
                    role === 'bowlers' ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Target className="w-4 h-4" /> Bowlers (10)
                </button>
              </div>
            </div>

            {/* Players Grid with real downloaded photos */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {playersList.map((p: any) => {
                const isClutch = p.archetype.includes('Clutch');
                return (
                  <div
                    key={p.rank}
                    className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 backdrop-blur-md rounded-2xl overflow-hidden border border-[#1A2A44] hover:border-[#EA1A85]/60 hover:shadow-xl hover:shadow-[#EA1A85]/10 transition duration-300 flex flex-col justify-between group"
                  >
                    <div className="p-5">
                      <div className="flex items-start gap-4">
                        <div className="relative flex-shrink-0">
                          <img
                            src={p.image.startsWith('/') ? p.image : `/${p.image}`}
                            alt={p.name}
                            className="w-16 h-16 rounded-2xl object-cover border-2 border-[#EA1A85]/50 shadow-lg group-hover:scale-105 transition"
                            onError={(e) => {
                              (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(p.name)}&background=EA1A85&color=fff&size=128&bold=true`;
                            }}
                          />
                          <span className="absolute -top-2 -left-2 w-6 h-6 rounded-full bg-[#EA1A85] text-white font-mono font-bold text-xs flex items-center justify-center shadow">
                            #{p.rank}
                          </span>
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <span
                              className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                                isClutch
                                  ? 'bg-[#EA1A85]/20 text-[#FF3399] border-[#EA1A85]/40'
                                  : 'bg-[#00F5D4]/20 text-[#00F5D4] border-[#00F5D4]/40'
                              }`}
                            >
                              {p.archetype}
                            </span>
                            <span className="text-xs font-mono font-extrabold text-[#F59E0B]">
                              Score: {p.final_score}
                            </span>
                          </div>
                          <h3 className="text-base font-extrabold text-white mt-1 truncate">{p.name}</h3>
                          <p className="text-xs text-slate-400 truncate">{p.team}</p>
                        </div>
                      </div>

                      {/* Stat Metrics Strip */}
                      <div className="mt-4 grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44] text-center">
                        {role === 'batters' ? (
                          <>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">HP SR</p>
                              <p className="text-sm font-bold font-mono text-white">{p.hp_sr}</p>
                            </div>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">HP Avg</p>
                              <p className="text-sm font-bold font-mono text-white">{p.hp_avg}</p>
                            </div>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">Bdry %</p>
                              <p className="text-sm font-bold font-mono text-[#FF3399]">{p.hp_bdry_pct}%</p>
                            </div>
                          </>
                        ) : (
                          <>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">HP Econ</p>
                              <p className="text-sm font-bold font-mono text-[#00F5D4]">{p.hp_econ}</p>
                            </div>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">HP WSR</p>
                              <p className="text-sm font-bold font-mono text-white">{p.hp_wsr}</p>
                            </div>
                            <div>
                              <p className="text-[10px] uppercase text-slate-400 font-semibold">Post-Bdry</p>
                              <p className="text-sm font-bold font-mono text-emerald-400">{p.post_bdry_comp}%</p>
                            </div>
                          </>
                        )}
                      </div>

                      {/* Complete Scouting Bio snippet */}
                      <p className="text-xs text-slate-300 mt-3 leading-relaxed line-clamp-2">
                        {p.bio}
                      </p>
                    </div>

                    <div className="px-5 py-3 bg-[#0B1322]/70 border-t border-[#1A2A44] flex items-center justify-between">
                      <span className="text-xs text-slate-400 font-mono">
                        PPR: <strong className="text-white">{p.ppr}x</strong>
                      </span>
                      <button
                        onClick={() => setSelectedPlayer(p)}
                        className="text-xs font-bold text-[#FF3399] hover:text-white flex items-center gap-1 transition"
                      >
                        Scouting Report <ChevronRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* TAB 2: 4-QUADRANT MATRIX */}
        {activeTab === 'quadrants' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1A2A44]">
              <h2 className="text-2xl font-black text-white flex items-center gap-2">
                The 4-Quadrant Permutations Model
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Comparing Normal Match Performance against High-Pressure Performance to isolate true clutch masters.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-[#0F1A2E]/90 rounded-xl p-4 border-l-4 border-[#EA1A85] border border-[#1A2A44]">
                <span className="text-xs uppercase font-black text-[#FF3399] tracking-wider">Quadrant 1</span>
                <h3 className="text-base font-bold text-white mt-0.5">Clutch Giants</h3>
                <p className="text-xs text-slate-400 mt-1">Dominant across ALL match conditions. High normal score and high pressure score.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Buttler, Narine, Bumrah, David</div>
              </div>

              <div className="bg-[#0F1A2E]/90 rounded-xl p-4 border-l-4 border-[#00F5D4] border border-[#1A2A44]">
                <span className="text-xs uppercase font-black text-[#00F5D4] tracking-wider">Quadrant 2</span>
                <h3 className="text-base font-bold text-white mt-0.5">Crisis Specialists</h3>
                <p className="text-xs text-slate-400 mt-1">Elevate by +25% to +60% when the team is in trouble.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Pant, Wade, Faheem, Haris Rauf</div>
              </div>

              <div className="bg-[#0F1A2E]/90 rounded-xl p-4 border-l-4 border-amber-500 border border-[#1A2A44]">
                <span className="text-xs uppercase font-black text-amber-400 tracking-wider">Quadrant 3</span>
                <h3 className="text-base font-bold text-white mt-0.5">Front-Runners</h3>
                <p className="text-xs text-slate-400 mt-1">Accumulate stats in easy games, but dip sharply under pressure.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Aiden Markram, Shami, Brevis</div>
              </div>

              <div className="bg-[#0F1A2E]/90 rounded-xl p-4 border-l-4 border-slate-600 border border-[#1A2A44]">
                <span className="text-xs uppercase font-black text-slate-400 tracking-wider">Quadrant 4</span>
                <h3 className="text-base font-bold text-white mt-0.5">Strugglers</h3>
                <p className="text-xs text-slate-400 mt-1">Below average across both normal and pressure scenarios.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Lower order accumulators</div>
              </div>
            </div>

            {/* Visual Scatter Grid representation */}
            <div className="bg-[#0F1A2E]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-[#EA1A85]" /> Player Classification Distribution
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-[#0B1322] border border-[#EA1A85]/40 space-y-2">
                  <h4 className="text-sm font-bold text-[#FF3399]">Top Clutch Batters Distribution</h4>
                  <ul className="text-xs space-y-1 text-slate-300">
                    <li>• <strong>Naman Dhir</strong>: HP Score 91.8 | Normal 60.9 | PPR 1.51 (Clutch Giant)</li>
                    <li>• <strong>Shashank Singh</strong>: HP Score 93.5 | Normal 82.7 | PPR 1.13 (Clutch Giant)</li>
                    <li>• <strong>Rishabh Pant</strong>: HP Score 82.7 | Normal 59.5 | PPR 1.39 (Crisis Specialist)</li>
                    <li>• <strong>Matthew Wade</strong>: HP Score 79.1 | Normal 50.6 | PPR 1.56 (Crisis Specialist)</li>
                  </ul>
                </div>
                <div className="p-4 rounded-xl bg-[#0B1322] border border-[#00F5D4]/40 space-y-2">
                  <h4 className="text-sm font-bold text-[#00F5D4]">Top Clutch Bowlers Distribution</h4>
                  <ul className="text-xs space-y-1 text-slate-300">
                    <li>• <strong>Sunil Narine</strong>: HP Score 82.5 | Normal 68.9 | PPR 1.20 (Clutch Giant)</li>
                    <li>• <strong>Jasprit Bumrah</strong>: HP Score 77.6 | Normal 68.0 | PPR 1.14 (Clutch Giant)</li>
                    <li>• <strong>Faheem Ashraf</strong>: HP Score 74.9 | Normal 39.7 | PPR 1.60 (Crisis Specialist)</li>
                    <li>• <strong>Riley Meredith</strong>: HP Score 68.5 | Normal 29.9 | PPR 1.60 (Crisis Specialist)</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 3: PRESSURE PROOF XI (FULL TEXT & SCOUTING BUTTONS - REQUEST 2) */}
        {activeTab === 'lineup' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1A2A44]">
              <h2 className="text-2xl font-black text-white flex items-center gap-2">
                The Pressure-Proof World XI <span className="text-[#F59E0B] text-base font-bold">• Master Lineup</span>
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Synthesized from positional optimization (Slots 1–7) and phase-specific bowling metrics. Click any card for the full scouting report.
              </p>
            </div>

            <div className="bg-gradient-to-br from-[#0F1A2E]/95 to-[#0B1322]/95 rounded-3xl p-6 sm:p-8 border-2 border-[#EA1A85]/30 space-y-8">
              
              {/* Batting slots 1 to 7 */}
              <div>
                <h3 className="text-sm uppercase tracking-wider font-extrabold text-slate-300 mb-4 flex items-center gap-2">
                  <Shield className="w-4 h-4 text-[#EA1A85]" /> Positional Batting Order (Slots 1 to 7)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {cricketData.pressure_proof_xi.batting_lineup.map((b: any) => (
                    <div key={b.slot} className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl overflow-hidden border border-[#1A2A44] hover:border-[#EA1A85]/60 flex flex-col justify-between transition group h-full shadow-lg">
                      <div className="p-5">
                        {/* Header: Slot & Image & Info */}
                        <div className="flex items-start gap-4">
                          <div className="relative flex-shrink-0">
                            <img
                              src={b.image.startsWith('/') ? b.image : `/${b.image}`}
                              alt={b.name}
                              className="w-16 h-16 rounded-2xl object-cover border-2 border-[#EA1A85]/50 shadow-lg group-hover:scale-105 transition"
                              onError={(e) => {
                                (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(b.name)}&background=EA1A85&color=fff&size=128&bold=true`;
                              }}
                            />
                            <span className="absolute -top-2 -left-2 w-7 h-7 rounded-full bg-[#EA1A85] text-white font-mono font-bold text-xs flex items-center justify-center shadow">
                              #{b.slot}
                            </span>
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="flex justify-between items-center">
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border border-[#EA1A85]/40 bg-[#EA1A85]/15 text-[#FF3399]">
                                {b.archetype || 'Clutch Giant'}
                              </span>
                              <span className="text-xs font-mono font-extrabold text-[#F59E0B]">Score: {b.score}</span>
                            </div>
                            <h4 className="text-base font-extrabold text-white truncate mt-1">{b.name}</h4>
                            <p className="text-xs text-slate-400 truncate">{b.role}</p>
                          </div>
                        </div>

                        {/* Metric Strip */}
                        <div className="mt-4 grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44] text-center">
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">HP SR</p>
                            <p className="text-sm font-bold font-mono text-white">{b.hp_sr}</p>
                          </div>
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">HP Avg</p>
                            <p className="text-sm font-bold font-mono text-white">{b.hp_avg}</p>
                          </div>
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">Slot Score</p>
                            <p className="text-sm font-bold font-mono text-[#FF3399]">{b.score}</p>
                          </div>
                        </div>

                        {/* Complete Scouting Bio snippet */}
                        <p className="text-xs text-slate-300 mt-3 leading-relaxed line-clamp-2">
                          {b.bio}
                        </p>
                      </div>

                      {/* Card Action Footer */}
                      <div className="px-5 py-3 bg-[#0B1322]/70 border-t border-[#1A2A44] flex items-center justify-between">
                        <span className="text-xs text-slate-400 font-mono">PPR: <strong className="text-white">{b.ppr}x</strong></span>
                        <button
                          onClick={() => setSelectedPlayer(b)}
                          className="text-xs font-bold text-[#FF3399] hover:text-white flex items-center gap-1 transition"
                        >
                          Scouting Report <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bowling Specialists */}
              <div>
                <h3 className="text-sm uppercase tracking-wider font-extrabold text-slate-300 mb-4 flex items-center gap-2">
                  <Crosshair className="w-4 h-4 text-[#00F5D4]" /> Phase-Specialist Bowling Attack
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {cricketData.pressure_proof_xi.bowling_attack.map((bw: any) => (
                    <div key={bw.role} className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl overflow-hidden border border-[#1A2A44] hover:border-[#00F5D4]/60 flex flex-col justify-between transition group h-full shadow-lg">
                      <div className="p-5">
                        {/* Header: Role & Image & Info */}
                        <div className="flex items-start gap-4">
                          <div className="relative flex-shrink-0">
                            <img
                              src={bw.image.startsWith('/') ? bw.image : `/${bw.image}`}
                              alt={bw.name}
                              className="w-16 h-16 rounded-2xl object-cover border-2 border-[#00F5D4]/50 shadow-lg group-hover:scale-105 transition"
                              onError={(e) => {
                                (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(bw.name)}&background=00F5D4&color=000&size=128&bold=true`;
                              }}
                            />
                            <span className="absolute -top-2 -left-2 px-2 py-0.5 rounded-full bg-[#00F5D4] text-slate-900 font-mono font-black text-[9px] flex items-center justify-center shadow uppercase">
                              PHASE
                            </span>
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="flex justify-between items-center">
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border border-[#00F5D4]/40 bg-[#00F5D4]/15 text-[#00F5D4]">
                                {bw.role}
                              </span>
                              <span className="text-xs font-mono font-extrabold text-[#F59E0B]">Score: {bw.score}</span>
                            </div>
                            <h4 className="text-base font-extrabold text-white mt-1 truncate">{bw.name}</h4>
                            <p className="text-xs text-slate-400 truncate">{bw.team}</p>
                          </div>
                        </div>

                        {/* Metric Strip */}
                        <div className="mt-4 grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44] text-center">
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">HP Econ</p>
                            <p className="text-sm font-bold font-mono text-[#00F5D4]">{bw.hp_econ}</p>
                          </div>
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">HP WSR</p>
                            <p className="text-sm font-bold font-mono text-white">{bw.hp_wsr}</p>
                          </div>
                          <div>
                            <p className="text-[10px] uppercase text-slate-400 font-semibold">Post-Bdry</p>
                            <p className="text-sm font-bold font-mono text-emerald-400">{bw.post_b_comp}%</p>
                          </div>
                        </div>

                        {/* Complete Scouting Bio snippet */}
                        <p className="text-xs text-slate-300 mt-3 leading-relaxed line-clamp-2">
                          {bw.bio}
                        </p>
                      </div>

                      {/* Card Action Footer */}
                      <div className="px-5 py-3 bg-[#0B1322]/70 border-t border-[#1A2A44] flex items-center justify-between">
                        <span className="text-xs text-slate-400 font-mono">PPR: <strong className="text-white">{bw.ppr}x</strong></span>
                        <button
                          onClick={() => setSelectedPlayer(bw)}
                          className="text-xs font-bold text-[#00F5D4] hover:text-white flex items-center gap-1 transition"
                        >
                          Scouting Report <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 4: SIMULATOR (ZERO EMOJI STICKERS) */}
        {activeTab === 'simulator' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1A2A44]">
              <h2 className="text-2xl font-black text-white flex items-center gap-2">
                Live Crunch-Time Pressure Simulator
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Adjust live game parameters to simulate high-stress match scenarios and see how our quantitative engine evaluates player pressure.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Left Controls */}
              <div className="lg:col-span-2 bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Sliders className="w-5 h-5 text-[#EA1A85]" /> Match Situation Inputs
                </h3>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-semibold text-slate-200">Required Run Rate (RRR)</label>
                    <span className="text-base font-mono font-bold text-[#FF3399]">{rrr.toFixed(1)} RPO</span>
                  </div>
                  <input
                    type="range"
                    min="4"
                    max="20"
                    step="0.5"
                    value={rrr}
                    onChange={(e) => setRrr(parseFloat(e.target.value))}
                    className="w-full accent-[#EA1A85] bg-[#0B1322] rounded-lg cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-slate-500 mt-1 font-medium">
                    <span>4.0 (Comfortable)</span>
                    <span>10.0 (Tense)</span>
                    <span>20.0 (Extreme Miracle)</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-semibold text-slate-200">Balls Remaining</label>
                    <span className="text-base font-mono font-bold text-white">{balls} Balls</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="120"
                    step="1"
                    value={balls}
                    onChange={(e) => setBalls(parseInt(e.target.value))}
                    className="w-full accent-[#EA1A85] bg-[#0B1322] rounded-lg cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-slate-500 mt-1 font-medium">
                    <span>1 Ball (Final Ball)</span>
                    <span>30 Balls (Death)</span>
                    <span>120 Balls (Innings Start)</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-semibold text-slate-200">Wickets Fallen</label>
                    <span className="text-base font-mono font-bold text-amber-400">{wickets} Wickets</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="9"
                    step="1"
                    value={wickets}
                    onChange={(e) => setWickets(parseInt(e.target.value))}
                    className="w-full accent-[#EA1A85] bg-[#0B1322] rounded-lg cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-slate-500 mt-1 font-medium">
                    <span>0 (Full Batting Depth)</span>
                    <span>5 (Crisis Phase)</span>
                    <span>9 (Last Wicket)</span>
                  </div>
                </div>

                {/* SELECT DROPDOWN (CLEAN PROFESSIONAL TEXT - ZERO STICKERS) */}
                <div>
                  <label className="text-sm font-semibold text-slate-200 block mb-2">Macro Match Stakes Context</label>
                  <select
                    value={stakes}
                    onChange={(e) => setStakes(parseFloat(e.target.value))}
                    className="w-full p-3 bg-[#0B1322] border border-[#1A2A44] rounded-xl text-white font-semibold focus:outline-none focus:border-[#EA1A85]"
                  >
                    <option value="1.00">Tournament Final (IPL / ICC Championship) - [W_M = 1.00]</option>
                    <option value="0.95">Direct Knockout / Semi-Final / Eliminator - [W_M = 0.95]</option>
                    <option value="0.85">Tied Series Decider (34 Matches) - [W_M = 0.85]</option>
                    <option value="0.80">Marquee Rivalry Derby (IND vs PAK, MI vs CSK) - [W_M = 0.80]</option>
                    <option value="0.70">Late League Match (Match 55+ NRR Battle) - [W_M = 0.70]</option>
                    <option value="0.50">Standard League Match - [W_M = 0.50]</option>
                    <option value="0.35">Dead Rubber (Series Already Clinched) - [W_M = 0.35]</option>
                  </select>
                </div>

                <div className="flex items-center space-x-3 p-3 bg-[#0B1322] rounded-xl border border-[#1A2A44]">
                  <input
                    type="checkbox"
                    id="fortress-check"
                    checked={isFortress}
                    onChange={(e) => setIsFortress(e.target.checked)}
                    className="w-4 h-4 accent-[#EA1A85] rounded cursor-pointer"
                  />
                  <label htmlFor="fortress-check" className="text-sm font-semibold text-slate-200 cursor-pointer">
                    Hostile Away Fortress Match (Wankhede, Eden Gardens, Gabba, MCG)
                  </label>
                </div>
              </div>

              {/* Gauge & Output */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] flex flex-col justify-between text-center">
                <div>
                  <span className="text-xs uppercase font-extrabold text-slate-400 tracking-wider">
                    Instantaneous Pressure Score
                  </span>
                  <div className="my-6">
                    <div className="text-6xl font-black font-mono text-[#EA1A85]">
                      {pBall.toFixed(2)}
                    </div>
                    <p className={`text-sm font-extrabold uppercase tracking-widest mt-2 ${pBall >= 0.70 ? 'text-[#FF3399]' : 'text-emerald-400'}`}>
                      {pBall >= 0.70 ? 'HIGH PRESSURE REGIME (70th+ %ile)' : 'NORMAL MATCH LEVERAGE REGIME'}
                    </p>
                  </div>

                  <div className="w-full bg-[#0B1322] h-3.5 rounded-full overflow-hidden p-0.5 border border-[#1A2A44] mb-4">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-400 via-amber-400 to-[#EA1A85] transition-all duration-300"
                      style={{ width: `${pPercent}%` }}
                    />
                  </div>

                  <div className="p-4 rounded-xl bg-[#0B1322]/60 border border-[#1A2A44] text-left">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">Engine Recommendation</span>
                    <p className="text-xs text-slate-200 mt-1 leading-relaxed">
                      {pBall >= 0.70 ? (
                        <>Deploy <strong>Naman Dhir</strong> (HP SR 187.5) or <strong>Shashank Singh</strong> (HP Avg 38.1). For bowling, immediately hand ball to <strong>Sunil Narine</strong> (HP Econ 6.76) or <strong>Jasprit Bumrah</strong> (Post-Bdry Composure 46.8%).</>
                      ) : (
                        <>Standard tactical rotation. <strong>Virat Kohli</strong> and <strong>Jos Buttler</strong> can build partnerships with low immediate risk.</>
                      )}
                    </p>
                  </div>
                </div>

                <div className="pt-4 border-t border-[#1A2A44] text-xs text-slate-500 font-mono">
                  P = 0.40 · C_macro + 0.60 · S_micro
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 5: METHODOLOGY (CLEAR & COMPREHENSIVE - REQUEST 4) */}
        {activeTab === 'methodology' && (
          <section className="space-y-8">
            <div className="pb-4 border-b border-[#1A2A44]">
              <h2 className="text-2xl font-black text-white flex items-center gap-2">
                Methodology & Mathematical Engine
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Complete transparent formulation of how 200,999 deliveries were evaluated to isolate true clutch execution from reputation.
              </p>
            </div>

            {/* Architecture Overview Banner (Clean, Executive & Human-Like) */}
            <div className="bg-gradient-to-br from-[#0F1A2E] to-[#0B1322] rounded-2xl p-6 border-l-4 border-[#EA1A85] border border-[#1A2A44] shadow-xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                <h3 className="text-base font-extrabold text-white flex items-center gap-2.5">
                  <Compass className="w-5 h-5 text-[#EA1A85]" /> The Core Analytics Philosophy
                </h3>
                <span className="px-2.5 py-1 rounded-full bg-[#EA1A85]/15 text-[#FF3399] border border-[#EA1A85]/30 text-[11px] font-bold w-fit">
                  Context-First Evaluation
                </span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                Traditional cricket statistics suffer from severe <strong>context-blindness</strong>: smashing a boundary when needing 15 runs off the final 4 deliveries of an IPL final carries infinitely greater consequence than hitting one in the powerplay of a dead rubber.
              </p>
              <p className="text-sm text-slate-300 leading-relaxed mt-2.5">
                Our quantitative framework reconstructs the true leverage of all <strong>200,999 deliveries</strong> by isolating two distinct forces: high-stakes macro match consequence and live micro in-game leverage. By benchmarking each player's execution in high-pressure crunch time against their routine baseline performance, we objectively separate world-class clutch performers from flat-track accumulators.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* STEP 1 */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4 hover:border-[#EA1A85]/50 transition">
                <div className="flex items-center gap-2 text-[#EA1A85] font-bold">
                  <span className="w-7 h-7 rounded-lg bg-[#EA1A85]/20 text-[#FF3399] flex items-center justify-center font-mono text-sm border border-[#EA1A85]/30">1</span>
                  <h3 className="text-base text-white">The Composite Pressure Index</h3>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Every legal delivery is assigned an instantaneous pressure value from 0.00 to 1.00 uniting two independent forces:
                </p>
                <div className="p-3.5 rounded-xl bg-[#0B1322] text-xs font-bold text-[#FF3399] border border-[#1A2A44] text-center flex items-center justify-center gap-2 flex-wrap">
                  <span className="px-2.5 py-1 rounded-lg bg-[#EA1A85]/20 text-[#FF3399] border border-[#EA1A85]/30">40% Macro Match Stakes</span>
                  <span className="text-slate-400 font-black">+</span>
                  <span className="px-2.5 py-1 rounded-lg bg-[#00F5D4]/20 text-[#00F5D4] border border-[#00F5D4]/30">60% Live Match Leverage</span>
                </div>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  <li><strong>Macro Stakes (40%)</strong>: Pre-game tournament context, knockout urgency, opponent quality, and venue hostility.</li>
                  <li><strong>Live In-Game Leverage (60%)</strong>: Ball-by-ball tension driven by dynamic required run rate, balls remaining, and wickets lost.</li>
                  <li><strong>Super Overs</strong>: Automatically scored at maximum intensity (1.00 Pressure).</li>
                  <li><strong>The 70th Percentile Cutoff</strong>: Deliveries with a pressure index of 0.70 or higher isolate the <strong>High-Pressure Regime</strong> (60,314 deliveries).</li>
                </ul>
              </div>

              {/* STEP 2 */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4 hover:border-[#00F5D4]/50 transition">
                <div className="flex items-center gap-2 text-[#00F5D4] font-bold">
                  <span className="w-7 h-7 rounded-lg bg-[#00F5D4]/20 text-[#00F5D4] flex items-center justify-center font-mono text-sm border border-[#00F5D4]/30">2</span>
                  <h3 className="text-base text-white">Macro Stakes Taxonomy</h3>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Calculated before the delivery is bowled to reflect the severity of match consequences:
                </p>
                <div className="p-3.5 rounded-xl bg-[#0B1322] text-xs font-bold text-[#00F5D4] border border-[#1A2A44] text-center flex items-center justify-center gap-2 flex-wrap">
                  <span className="px-2 py-0.5 rounded bg-[#00F5D4]/20 text-[#00F5D4]">50% Match Consequence</span>
                  <span className="text-slate-400">+</span>
                  <span className="px-2 py-0.5 rounded bg-[#F59E0B]/20 text-[#F59E0B]">35% Opposition Tier</span>
                  <span className="text-slate-400">+</span>
                  <span className="px-2 py-0.5 rounded bg-[#EA1A85]/20 text-[#FF3399]">15% Away Fortress</span>
                </div>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  <li><strong>Championship Finals (1.00 Weight)</strong>: 15 winner-take-all tournament finals.</li>
                  <li><strong>Direct Knockouts (0.95 Weight)</strong>: 9 sudden-death eliminators and semi-finals.</li>
                  <li><strong>Tied Series Deciders (0.85 Weight)</strong>: 34 winner-take-all bilateral deciders tied at 1–1 or 2–2.</li>
                  <li><strong>Marquee Rivalries (+0.15 Boost)</strong>: India vs Pakistan, Mumbai Indians vs CSK, Australia vs England.</li>
                  <li><strong>Dead Rubbers (0.35 Weight)</strong>: 64 low-leverage matches played after series or playoff qualification was secured.</li>
                </ul>
              </div>

              {/* STEP 3 */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4 hover:border-[#F59E0B]/50 transition">
                <div className="flex items-center gap-2 text-[#F59E0B] font-bold">
                  <span className="w-7 h-7 rounded-lg bg-[#F59E0B]/20 text-[#F59E0B] flex items-center justify-center font-mono text-sm border border-[#F59E0B]/30">3</span>
                  <h3 className="text-base text-white">Opposition Quality Hierarchy (Q_opp)</h3>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Calibrated on empirical win-loss records and ICC silverware between 2022 and 2026:
                </p>
                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                    <span className="text-[#F59E0B] font-bold block">Tier 1.0 (1.00)</span>
                    <span className="text-slate-300 text-[11px]">India (82 wins, 2 T20 WCs)</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                    <span className="text-[#FF3399] font-bold block">Tier 1.5 (0.88-0.92)</span>
                    <span className="text-slate-300 text-[11px]">IPL Franchises</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                    <span className="text-[#00F5D4] font-bold block">Tier 2.0 (0.85)</span>
                    <span className="text-slate-300 text-[11px]">Australia, England, SA, NZ</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                    <span className="text-slate-400 font-bold block">Tier 3.0 (0.70)</span>
                    <span className="text-slate-300 text-[11px]">Pakistan, WI, SL, Afghanistan</span>
                  </div>
                </div>
              </div>

              {/* STEP 4 */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4 hover:border-emerald-400/50 transition">
                <div className="flex items-center gap-2 text-emerald-400 font-bold">
                  <span className="w-7 h-7 rounded-lg bg-emerald-400/20 text-emerald-400 flex items-center justify-center font-mono text-sm border border-emerald-400/30">4</span>
                  <h3 className="text-base text-white">Psychological Momentum Indicators</h3>
                </div>
                <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside leading-relaxed">
                  <li><strong>Post-Boundary Stress (Composure)</strong>: Evaluates what a bowler executes on the ball immediately following a 4 or 6. Jasprit Bumrah (46.8%) and Sunil Narine (40.0%) lead the tournament in comeback dot and wicket rate.</li>
                  <li><strong>Post-Wicket Leverage Surge</strong>: Incoming batters face an immediate +8% pressure surge for the next 6 balls as fielding momentum rises.</li>
                  <li><strong>3-Match Rolling Form</strong>: Incorporates a 3-match recent trajectory to account for match fitness, confidence, and fatigue.</li>
                </ul>
              </div>

              {/* STEP 5 */}
              <div className="bg-gradient-to-br from-[#0F1A2E]/90 to-[#0B1322]/90 rounded-2xl p-6 border border-[#1A2A44] space-y-4 md:col-span-2">
                <div className="flex items-center gap-2 text-[#FF3399] font-bold">
                  <span className="w-7 h-7 rounded-lg bg-[#EA1A85]/20 text-[#FF3399] flex items-center justify-center font-mono text-sm border border-[#EA1A85]/30">5</span>
                  <h3 className="text-base text-white">Performance Scoring Equations & Weights</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* Batters formula */}
                  <div className="p-4 rounded-xl bg-[#0B1322] border border-[#1A2A44] space-y-2">
                    <h4 className="text-xs uppercase font-extrabold text-[#EA1A85] tracking-wider">Batting Performance Equation</h4>
                    <p className="text-xs font-mono text-slate-200 bg-[#0F1A2E] p-2 rounded border border-[#1A2A44]">
                      Score = 30% Strike Rate + 25% Boundary% + 18% Strike Rotation + 17% Average + 10% Dot Avoidance
                    </p>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Prioritizes <strong>Boundary Conversion (25%)</strong> over strike rotation (18%) per franchise rules, since high-pressure death overs demand maximum boundaries.
                    </p>
                  </div>

                  {/* Bowlers formula */}
                  <div className="p-4 rounded-xl bg-[#0B1322] border border-[#1A2A44] space-y-2">
                    <h4 className="text-xs uppercase font-extrabold text-[#00F5D4] tracking-wider">Bowling Performance Equation</h4>
                    <p className="text-xs font-mono text-slate-200 bg-[#0F1A2E] p-2 rounded border border-[#1A2A44]">
                      Score = 30% Economy + 25% Wicket Strike Rate + 20% Post-Boundary Composure + 15% Dot% + 10% Opposition Tier
                    </p>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Rewards <strong>low economy (30%)</strong> and <strong>wicket-taking strike rate (25%)</strong> alongside <strong>post-boundary bounce-back composure (20%)</strong>.
                    </p>
                  </div>
                </div>

                {/* Elevation Ratio */}
                <div className="p-4 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                  <h4 className="text-xs uppercase font-extrabold text-[#F59E0B] tracking-wider mb-1">Pressure Performance Ratio (PPR)</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Measures how much a player elevates compared to normal conditions: <strong>PPR = High-Pressure Score / Baseline Score</strong>. A ratio of 1.51x (achieved by Naman Dhir) represents a +51% performance surge under pressure, while a ratio of 0.79x (e.g. Sam Curran as a bowler) represents a -21% decline under pressure.
                  </p>
                </div>
              </div>

            </div>
          </section>
        )}

      </main>

      {/* SCOUTING MODAL */}
      {selectedPlayer && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#0F1A2E] rounded-3xl max-w-lg w-full p-6 sm:p-8 relative border border-[#EA1A85]/50 shadow-2xl shadow-[#EA1A85]/25 overflow-hidden space-y-4">
            <button
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 w-9 h-9 rounded-full bg-[#0B1322] hover:bg-[#1A2A44] flex items-center justify-center text-slate-300 hover:text-white transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-4 border-b border-[#1A2A44] pb-4">
              <img
                src={selectedPlayer.image.startsWith('/') ? selectedPlayer.image : `/${selectedPlayer.image}`}
                alt={selectedPlayer.name}
                className="w-20 h-20 rounded-2xl object-cover border-2 border-[#EA1A85] shadow-lg flex-shrink-0"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(selectedPlayer.name)}&background=EA1A85&color=fff&size=128&bold=true`;
                }}
              />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#EA1A85] text-white">
                    {selectedPlayer.slot ? `Slot #${selectedPlayer.slot}` : (selectedPlayer.rank ? `Rank #${selectedPlayer.rank}` : selectedPlayer.role)}
                  </span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-[#0B1322] text-[#00F5D4] border border-[#1A2A44]">
                    {selectedPlayer.archetype || 'Clutch Giant'}
                  </span>
                </div>
                <h3 className="text-xl font-black text-white mt-1">{selectedPlayer.name}</h3>
                <p className="text-xs text-slate-400">{selectedPlayer.role || selectedPlayer.team}</p>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs uppercase font-extrabold text-[#FF3399] tracking-wider">
                Tactical Scouting Assessment
              </h4>
              <p className="text-sm text-slate-200 leading-relaxed">{selectedPlayer.bio}</p>

              <div className="p-3.5 rounded-xl bg-[#0B1322] border border-[#1A2A44]">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Key Super-Power</span>
                <p className="text-xs font-bold text-[#00F5D4] mt-0.5">{selectedPlayer.key_strength || 'High-Pressure Execution'}</p>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono pt-2">
                <div className="p-2.5 rounded-lg bg-[#0B1322] border border-[#1A2A44]">
                  <span className="text-slate-400 block text-[10px]">BASELINE (NORMAL) SCORE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedPlayer.norm_sr || selectedPlayer.norm_econ || 'Standard'}
                  </span>
                </div>
                <div className="p-2.5 rounded-lg bg-[#0B1322] border border-[#EA1A85]/30">
                  <span className="text-[#FF3399] block text-[10px]">HIGH-PRESSURE SCORE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedPlayer.hp_sr || selectedPlayer.hp_econ || selectedPlayer.score}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className="mt-16 border-t border-[#1A2A44] bg-[#050811]/95 py-8 text-center text-xs text-slate-500 relative z-10">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#EA1A85] animate-pulse"></span>
            <span className="font-bold text-slate-400">Rajasthan Royals SupeRR Selector • Round 1 Official Submission</span>
          </div>
          <div className="font-medium">
            Built with Next.js, Tailwind CSS & Audited Python Data Science Pipeline
          </div>
        </div>
      </footer>

    </div>
  );
}
