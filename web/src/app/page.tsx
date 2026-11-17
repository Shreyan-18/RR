'use client';

import React, { useState } from 'react';
import cricketData from '@/data/cricket_data.json';
import { 
  Trophy, 
  LayoutGrid, 
  Shield, 
  Gauge, 
  FileText, 
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
  Brain
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
    <div className="min-h-screen bg-[#060B14] text-slate-100 font-sans selection:bg-[#EA1A85] selection:text-white pb-16">
      
      {/* HEADER / NAVIGATION */}
      <header className="sticky top-0 z-50 bg-[#060B14]/90 backdrop-blur-md border-b border-[#1F314F]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-[#EA1A85] to-[#001C58] flex items-center justify-center font-extrabold text-white text-xl shadow-lg shadow-[#EA1A85]/30 border border-[#EA1A85]/40">
              RR
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded-full bg-[#EA1A85]/20 text-[#FF4DAB] font-bold border border-[#EA1A85]/30">
                  Season 2 • Round 1
                </span>
                <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded-full bg-[#00F5D4]/10 text-[#00F5D4] font-bold border border-[#00F5D4]/20">
                  Verified Pipeline
                </span>
              </div>
              <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                SupeRR Selector <span className="text-[#EA1A85]">Analytics Hub</span>
              </h1>
            </div>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center space-x-1 bg-[#0F1A2E] p-1.5 rounded-xl border border-[#1F314F]">
            <button
              onClick={() => setActiveTab('leaderboard')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'leaderboard'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#152238]'
              }`}
            >
              <Trophy className="w-4 h-4" /> Leaderboard
            </button>
            <button
              onClick={() => setActiveTab('quadrants')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'quadrants'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#152238]'
              }`}
            >
              <LayoutGrid className="w-4 h-4" /> 4-Quadrant
            </button>
            <button
              onClick={() => setActiveTab('lineup')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'lineup'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#152238]'
              }`}
            >
              <Shield className="w-4 h-4" /> Pressure-Proof XI
            </button>
            <button
              onClick={() => setActiveTab('simulator')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'simulator'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#152238]'
              }`}
            >
              <Gauge className="w-4 h-4" /> Simulator
            </button>
            <button
              onClick={() => setActiveTab('methodology')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                activeTab === 'methodology'
                  ? 'bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/30'
                  : 'text-slate-400 hover:text-white hover:bg-[#152238]'
              }`}
            >
              <FileText className="w-4 h-4" /> Methodology
            </button>
          </nav>

          {/* Quick link */}
          <div className="flex items-center space-x-3">
            <a
              href="https://github.com/Shreyan-18/RR.git"
              target="_blank"
              rel="noreferrer"
              className="px-3.5 py-2 rounded-lg bg-[#152238] hover:bg-[#1F314F] text-slate-200 text-xs font-bold border border-[#1F314F] transition flex items-center gap-1.5"
            >
              <Github className="w-4 h-4" /> GitHub
            </a>
          </div>
        </div>

        {/* Mobile Navigation Bar */}
        <div className="md:hidden flex overflow-x-auto px-4 py-2.5 space-x-2 bg-[#0F1A2E] border-t border-[#1F314F]">
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* STATS STRIP */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-[#152238]/70 backdrop-blur-md rounded-2xl p-4 border border-[#1F314F] relative overflow-hidden">
            <Database className="w-16 h-16 absolute right-2 -bottom-2 text-[#EA1A85]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">Total Deliveries</p>
            <p className="text-2xl sm:text-3xl font-extrabold font-mono text-white mt-1">200,999</p>
            <span className="text-xs text-[#FF4DAB] font-semibold mt-1 inline-block">867 Matches (IPL & T20I)</span>
          </div>

          <div className="bg-[#152238]/70 backdrop-blur-md rounded-2xl p-4 border border-[#1F314F] relative overflow-hidden">
            <Flame className="w-16 h-16 absolute right-2 -bottom-2 text-[#00F5D4]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">High Pressure Split</p>
            <p className="text-2xl sm:text-3xl font-extrabold font-mono text-[#00F5D4] mt-1">60,314</p>
            <span className="text-xs text-slate-300 font-semibold mt-1 inline-block">Top 30% Leverage (P ≥ 0.70)</span>
          </div>

          <div className="bg-[#152238]/70 backdrop-blur-md rounded-2xl p-4 border border-[#1F314F] relative overflow-hidden">
            <Users className="w-16 h-16 absolute right-2 -bottom-2 text-[#D4AF37]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">Qualified Players</p>
            <p className="text-2xl sm:text-3xl font-extrabold font-mono text-white mt-1">405</p>
            <span className="text-xs text-[#D4AF37] font-semibold mt-1 inline-block">162 Batters • 243 Bowlers</span>
          </div>

          <div className="bg-[#152238]/70 backdrop-blur-md rounded-2xl p-4 border border-[#1F314F] relative overflow-hidden">
            <Crown className="w-16 h-16 absolute right-2 -bottom-2 text-[#EA1A85]/10" />
            <p className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">#1 Clutch Ranks</p>
            <p className="text-lg sm:text-xl font-extrabold text-white mt-1 truncate">N. Dhir & S. Narine</p>
            <span className="text-xs text-[#FF4DAB] font-semibold mt-1 inline-block">Scores: 87.7 (Bat) • 76.8 (Bowl)</span>
          </div>
        </section>

        {/* TAB 1: LEADERBOARDS */}
        {activeTab === 'leaderboard' && (
          <section className="space-y-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-[#1F314F]">
              <div>
                <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
                  Official Pressure Rankings <span className="text-[#EA1A85] text-base font-semibold">• Top 10</span>
                </h2>
                <p className="text-sm text-slate-400 mt-0.5">
                  Audited across 867 fixtures, prioritizing boundary conversion (27.5%), post-boundary composure (46.8%), and macro stakes.
                </p>
              </div>

              {/* Batters vs Bowlers Toggle */}
              <div className="flex items-center bg-[#0F1A2E] p-1 rounded-xl border border-[#1F314F]">
                <button
                  onClick={() => setRole('batters')}
                  className={`px-5 py-2 rounded-lg text-sm font-bold flex items-center gap-1.5 transition ${
                    role === 'batters' ? 'bg-[#EA1A85] text-white shadow-md' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Zap className="w-4 h-4" /> Batters (10)
                </button>
                <button
                  onClick={() => setRole('bowlers')}
                  className={`px-5 py-2 rounded-lg text-sm font-bold flex items-center gap-1.5 transition ${
                    role === 'bowlers' ? 'bg-[#EA1A85] text-white shadow-md' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Target className="w-4 h-4" /> Bowlers (10)
                </button>
              </div>
            </div>

            {/* Players Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {playersList.map((p: any) => {
                const isClutch = p.archetype.includes('Clutch');
                return (
                  <div
                    key={p.rank}
                    className="bg-[#152238]/70 backdrop-blur-md rounded-2xl overflow-hidden border border-[#1F314F] hover:border-[#EA1A85]/50 transition duration-300 flex flex-col justify-between group"
                  >
                    <div className="p-5">
                      <div className="flex items-start gap-4">
                        <div className="relative">
                          <img
                            src={p.image}
                            alt={p.name}
                            className="w-16 h-16 rounded-2xl object-cover border-2 border-[#EA1A85]/40 shadow-lg group-hover:scale-105 transition"
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
                                  ? 'bg-[#EA1A85]/20 text-[#FF4DAB] border-[#EA1A85]/40'
                                  : 'bg-[#00F5D4]/20 text-[#00F5D4] border-[#00F5D4]/40'
                              }`}
                            >
                              {p.archetype}
                            </span>
                            <span className="text-xs font-mono font-extrabold text-[#D4AF37]">
                              Score: {p.final_score}
                            </span>
                          </div>
                          <h3 className="text-base font-extrabold text-white mt-1 truncate">{p.name}</h3>
                          <p className="text-xs text-slate-400 truncate">{p.team}</p>
                        </div>
                      </div>

                      {/* Stat Metrics Strip */}
                      <div className="mt-4 grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-[#0F1A2E] text-center">
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
                              <p className="text-sm font-bold font-mono text-[#FF4DAB]">{p.hp_bdry_pct}%</p>
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

                      {/* Scouting Bio snippet */}
                      <p className="text-xs text-slate-300 mt-3 line-clamp-2 leading-relaxed italic">
                        "{p.bio}"
                      </p>
                    </div>

                    <div className="px-5 py-3 bg-[#0F1A2E]/60 border-t border-[#1F314F] flex items-center justify-between">
                      <span className="text-xs text-slate-400 font-mono">
                        PPR: <strong className="text-white">{p.ppr}x</strong>
                      </span>
                      <button
                        onClick={() => setSelectedPlayer(p)}
                        className="text-xs font-bold text-[#FF4DAB] hover:text-white flex items-center gap-1 transition"
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
            <div className="pb-4 border-b border-[#1F314F]">
              <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
                The 4-Quadrant Permutations Model
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Comparing Normal Match Performance against High-Pressure Performance to isolate true clutch masters.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-[#152238]/70 rounded-xl p-4 border-l-4 border-[#EA1A85] border border-[#1F314F]">
                <span className="text-xs uppercase font-extrabold text-[#FF4DAB]">Quadrant 1</span>
                <h3 className="text-base font-bold text-white mt-0.5">Clutch Giants</h3>
                <p className="text-xs text-slate-400 mt-1">Dominant across ALL match conditions. Consistent high scores.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Buttler, Narine, Bumrah, David</div>
              </div>

              <div className="bg-[#152238]/70 rounded-xl p-4 border-l-4 border-[#00F5D4] border border-[#1F314F]">
                <span className="text-xs uppercase font-extrabold text-[#00F5D4]">Quadrant 2</span>
                <h3 className="text-base font-bold text-white mt-0.5">Crisis Specialists</h3>
                <p className="text-xs text-slate-400 mt-1">Elevate by +25% to +60% when the team is in trouble.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Pant, Wade, Faheem, Haris Rauf</div>
              </div>

              <div className="bg-[#152238]/70 rounded-xl p-4 border-l-4 border-amber-500 border border-[#1F314F]">
                <span className="text-xs uppercase font-extrabold text-amber-400">Quadrant 3</span>
                <h3 className="text-base font-bold text-white mt-0.5">Front-Runners</h3>
                <p className="text-xs text-slate-400 mt-1">Accumulate stats in easy games, but dip sharply under pressure.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Aiden Markram, Shami, Brevis</div>
              </div>

              <div className="bg-[#152238]/70 rounded-xl p-4 border-l-4 border-slate-600 border border-[#1F314F]">
                <span className="text-xs uppercase font-extrabold text-slate-400">Quadrant 4</span>
                <h3 className="text-base font-bold text-white mt-0.5">Strugglers</h3>
                <p className="text-xs text-slate-400 mt-1">Below average across both normal and pressure scenarios.</p>
                <div className="mt-2 text-xs font-mono text-slate-300">Lower order accumulators</div>
              </div>
            </div>

            {/* Visual Scatter Grid representation */}
            <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-[#EA1A85]" /> Player Classification Map
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-[#0F1A2E] border border-[#EA1A85]/40 space-y-2">
                  <h4 className="text-sm font-bold text-[#FF4DAB]">Top Clutch Batters Distribution</h4>
                  <ul className="text-xs space-y-1 text-slate-300">
                    <li>• <strong>Naman Dhir</strong>: HP Score 91.8 | Normal 60.9 | PPR 1.51 (Clutch Giant)</li>
                    <li>• <strong>Shashank Singh</strong>: HP Score 93.5 | Normal 82.7 | PPR 1.13 (Clutch Giant)</li>
                    <li>• <strong>Rishabh Pant</strong>: HP Score 82.7 | Normal 59.5 | PPR 1.39 (Crisis Specialist)</li>
                    <li>• <strong>Matthew Wade</strong>: HP Score 79.1 | Normal 50.6 | PPR 1.56 (Crisis Specialist)</li>
                  </ul>
                </div>
                <div className="p-4 rounded-xl bg-[#0F1A2E] border border-[#00F5D4]/40 space-y-2">
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

        {/* TAB 3: PRESSURE PROOF XI */}
        {activeTab === 'lineup' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1F314F]">
              <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
                The Pressure-Proof World XI <span className="text-[#D4AF37] text-base font-semibold">• Master Lineup</span>
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Synthesized from positional optimization (Slots 1–7) and phase-specific bowling metrics.
              </p>
            </div>

            <div className="bg-[#152238]/70 rounded-3xl p-6 sm:p-8 border-2 border-[#EA1A85]/30 space-y-8">
              
              {/* Batting slots 1 to 7 */}
              <div>
                <h3 className="text-sm uppercase tracking-wider font-extrabold text-slate-300 mb-4 flex items-center gap-2">
                  <Shield className="w-4 h-4 text-[#EA1A85]" /> Positional Batting Order (Slots 1 to 7)
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {cricketData.pressure_proof_xi.batting_lineup.map((b: any) => (
                    <div key={b.slot} className="bg-[#0F1A2E] rounded-xl p-4 border border-[#1F314F] hover:border-[#EA1A85]/50 transition">
                      <div className="flex items-center gap-3">
                        <img
                          src={b.image}
                          alt={b.name}
                          className="w-12 h-12 rounded-xl object-cover border border-[#EA1A85]"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(b.name)}&background=EA1A85&color=fff&size=128&bold=true`;
                          }}
                        />
                        <div className="min-w-0 flex-1">
                          <div className="flex justify-between items-center">
                            <span className="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-[#EA1A85]/20 text-[#FF4DAB] font-mono">
                              Slot #{b.slot}
                            </span>
                            <span className="text-xs font-bold font-mono text-[#D4AF37]">{b.score}</span>
                          </div>
                          <h4 className="text-sm font-black text-white truncate mt-1">{b.name}</h4>
                          <p className="text-[10px] text-slate-400 truncate">{b.role}</p>
                        </div>
                      </div>
                      <p className="text-[11px] text-slate-300 mt-2.5 line-clamp-2 leading-relaxed">{b.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bowling Specialists */}
              <div>
                <h3 className="text-sm uppercase tracking-wider font-extrabold text-slate-300 mb-4 flex items-center gap-2">
                  <Crosshair className="w-4 h-4 text-[#00F5D4]" /> Phase-Specialist Bowling Attack
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {cricketData.pressure_proof_xi.bowling_attack.map((bw: any) => (
                    <div key={bw.role} className="bg-[#0F1A2E] rounded-xl p-4 border border-[#1F314F] hover:border-[#00F5D4]/50 transition">
                      <div className="flex items-center gap-3">
                        <img
                          src={bw.image}
                          alt={bw.name}
                          className="w-12 h-12 rounded-xl object-cover border border-[#00F5D4]"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(bw.name)}&background=00F5D4&color=000&size=128&bold=true`;
                          }}
                        />
                        <div className="min-w-0 flex-1">
                          <div className="flex justify-between items-center">
                            <span className="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-[#00F5D4]/20 text-[#00F5D4] font-mono">
                              {bw.role}
                            </span>
                            <span className="text-xs font-bold font-mono text-[#D4AF37]">{bw.score}</span>
                          </div>
                          <h4 className="text-sm font-black text-white truncate mt-1">{bw.name}</h4>
                          <p className="text-[10px] text-slate-400 truncate">{bw.team}</p>
                        </div>
                      </div>
                      <p className="text-[11px] text-slate-300 mt-2.5 line-clamp-2 leading-relaxed">{bw.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 4: SIMULATOR */}
        {activeTab === 'simulator' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1F314F]">
              <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
                Live Crunch-Time Pressure Simulator
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Tweak match parameters in real-time to compute the instantaneous Composite Pressure Index ($P$) and tactical recommendations.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Left Controls */}
              <div className="lg:col-span-2 bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Sliders className="w-5 h-5 text-[#EA1A85]" /> Match Situation Inputs
                </h3>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-semibold text-slate-200">Required Run Rate (RRR)</label>
                    <span className="text-base font-mono font-bold text-[#FF4DAB]">{rrr.toFixed(1)} RPO</span>
                  </div>
                  <input
                    type="range"
                    min="4"
                    max="20"
                    step="0.5"
                    value={rrr}
                    onChange={(e) => setRrr(parseFloat(e.target.value))}
                    className="w-full accent-[#EA1A85] bg-[#0F1A2E] rounded-lg cursor-pointer"
                  />
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
                    className="w-full accent-[#EA1A85] bg-[#0F1A2E] rounded-lg cursor-pointer"
                  />
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
                    className="w-full accent-[#EA1A85] bg-[#0F1A2E] rounded-lg cursor-pointer"
                  />
                </div>

                <div>
                  <label className="text-sm font-semibold text-slate-200 block mb-2">Macro Match Stakes</label>
                  <select
                    value={stakes}
                    onChange={(e) => setStakes(parseFloat(e.target.value))}
                    className="w-full p-3 bg-[#0F1A2E] border border-[#1F314F] rounded-xl text-white font-semibold focus:outline-none focus:border-[#EA1A85]"
                  >
                    <option value="1.00">🏆 Tournament Final (IPL / ICC Final) - W_M = 1.00</option>
                    <option value="0.95">⚔️ Direct Knockout / Semi-Final - W_M = 0.95</option>
                    <option value="0.85">🔥 Tied Series Decider (34 Matches) - W_M = 0.85</option>
                    <option value="0.80">💥 Marquee Derby (IND vs PAK, MI vs CSK) - W_M = 0.80</option>
                    <option value="0.70">📈 Late League Match (Match 55+) - W_M = 0.70</option>
                    <option value="0.50">🏏 Standard League Match - W_M = 0.50</option>
                    <option value="0.35">💤 Dead Rubber - W_M = 0.35</option>
                  </select>
                </div>

                <div className="flex items-center space-x-3 p-3 bg-[#0F1A2E] rounded-xl border border-[#1F314F]">
                  <input
                    type="checkbox"
                    id="fortress-check"
                    checked={isFortress}
                    onChange={(e) => setIsFortress(e.target.checked)}
                    className="w-4 h-4 accent-[#EA1A85] rounded cursor-pointer"
                  />
                  <label htmlFor="fortress-check" className="text-sm font-semibold text-slate-200 cursor-pointer">
                    Hostile Away Fortress (Wankhede, Eden Gardens, Gabba, MCG)
                  </label>
                </div>
              </div>

              {/* Gauge & Output */}
              <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] flex flex-col justify-between text-center">
                <div>
                  <span className="text-xs uppercase font-extrabold text-slate-400 tracking-wider">
                    Instantaneous Pressure Score
                  </span>
                  <div className="my-6">
                    <div className="text-6xl font-black font-mono text-[#EA1A85]">
                      {pBall.toFixed(2)}
                    </div>
                    <p className={`text-sm font-extrabold uppercase tracking-widest mt-2 ${pBall >= 0.70 ? 'text-[#FF4DAB]' : 'text-emerald-400'}`}>
                      {pBall >= 0.70 ? 'HIGH PRESSURE REGIME (70th+ %ile)' : 'NORMAL MATCH LEVERAGE REGIME'}
                    </p>
                  </div>

                  <div className="w-full bg-[#0F1A2E] h-3.5 rounded-full overflow-hidden p-0.5 border border-[#1F314F] mb-4">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-400 via-amber-400 to-[#EA1A85] transition-all duration-300"
                      style={{ width: `${pPercent}%` }}
                    />
                  </div>

                  <div className="p-4 rounded-xl bg-[#0F1A2E]/60 border border-[#1F314F] text-left">
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

                <div className="pt-4 border-t border-[#1F314F] text-xs text-slate-500 font-mono">
                  P = 0.40 · C_macro + 0.60 · S_micro
                </div>
              </div>
            </div>
          </section>
        )}

        {/* TAB 5: METHODOLOGY */}
        {activeTab === 'methodology' && (
          <section className="space-y-6">
            <div className="pb-4 border-b border-[#1F314F]">
              <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
                Mathematical Formulation & Domain Architecture
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Audited data-science pipeline adhering to all RR problem statement constraints.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-3">
                <div className="flex items-center gap-2 text-[#EA1A85] font-bold">
                  <Database className="w-5 h-5" />
                  <h3>1. The Composite Pressure Index</h3>
                </div>
                <div className="p-3 rounded-xl bg-[#0F1A2E] font-mono text-xs text-[#FF4DAB] border border-[#1F314F]">
                  P_ball = 0.40 * C_macro + 0.60 * S_micro
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Every ball across 200,999 deliveries receives a continuous pressure score. Top 30% ($P \ge 0.70$) forms the High-Pressure Regime. Super Overs hardcoded to 1.00.
                </p>
              </div>

              <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-3">
                <div className="flex items-center gap-2 text-[#00F5D4] font-bold">
                  <Trophy className="w-5 h-5" />
                  <h3>2. Macro Stakes & Deciders</h3>
                </div>
                <div className="p-3 rounded-xl bg-[#0F1A2E] font-mono text-xs text-[#00F5D4] border border-[#1F314F]">
                  C_macro = 0.50 * W_M + 0.35 * Q_opp + 0.15 * H_fortress
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Incorporates 15 tournament finals, 9 direct knockouts, 34 tied bilateral series deciders, 48 high-ego rivalries (IND vs PAK, MI vs CSK), and 64 dead rubbers.
                </p>
              </div>

              <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-3">
                <div className="flex items-center gap-2 text-[#D4AF37] font-bold">
                  <Award className="w-5 h-5" />
                  <h3>3. Opposition Quality Tiers</h3>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="p-2 rounded bg-[#0F1A2E] border border-[#1F314F]"><span className="text-[#D4AF37] font-bold">Tier 1 (1.00)</span>: India</div>
                  <div className="p-2 rounded bg-[#0F1A2E] border border-[#1F314F]"><span className="text-[#FF4DAB] font-bold">Tier 1.5 (0.88-0.92)</span>: IPL</div>
                  <div className="p-2 rounded bg-[#0F1A2E] border border-[#1F314F]"><span className="text-[#00F5D4] font-bold">Tier 2 (0.85)</span>: AUS, ENG, SA, NZ</div>
                  <div className="p-2 rounded bg-[#0F1A2E] border border-[#1F314F]"><span className="text-slate-400 font-bold">Tier 3 (0.70)</span>: PAK, WI, SL, AFG</div>
                </div>
              </div>

              <div className="bg-[#152238]/70 rounded-2xl p-6 border border-[#1F314F] space-y-3">
                <div className="flex items-center gap-2 text-emerald-400 font-bold">
                  <Brain className="w-5 h-5" />
                  <h3>4. Psychological Momentum Indicators</h3>
                </div>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside leading-relaxed">
                  <li><strong>Post-Boundary Stress</strong>: Bowler dot/wicket comeback rate after conceding a 4/6. Bumrah (46.8%) and Narine (40.0%) lead.</li>
                  <li><strong>Post-Wicket Surge</strong>: Next 6 balls receive +0.08 pressure boost.</li>
                  <li><strong>3-Match Rolling Form</strong>: Accounts for fatigue and recent form swings.</li>
                </ul>
              </div>
            </div>
          </section>
        )}

      </main>

      {/* SCOUTING MODAL */}
      {selectedPlayer && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#152238] rounded-3xl max-w-lg w-full p-6 sm:p-8 relative border border-[#EA1A85]/40 shadow-2xl shadow-[#EA1A85]/20 overflow-hidden space-y-4">
            <button
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 w-9 h-9 rounded-full bg-[#0F1A2E] hover:bg-[#1F314F] flex items-center justify-center text-slate-300 hover:text-white transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-4 border-b border-[#1F314F] pb-4">
              <img
                src={selectedPlayer.image}
                alt={selectedPlayer.name}
                className="w-20 h-20 rounded-2xl object-cover border-2 border-[#EA1A85] shadow-lg"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(selectedPlayer.name)}&background=EA1A85&color=fff&size=128&bold=true`;
                }}
              />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#EA1A85] text-white">
                    Rank #{selectedPlayer.rank}
                  </span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-[#0F1A2E] text-[#00F5D4] border border-[#1F314F]">
                    {selectedPlayer.archetype}
                  </span>
                </div>
                <h3 className="text-xl font-black text-white mt-1">{selectedPlayer.name}</h3>
                <p className="text-xs text-slate-400">{selectedPlayer.role} • {selectedPlayer.team}</p>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs uppercase font-extrabold text-[#FF4DAB] tracking-wider">
                Tactical Scouting Assessment
              </h4>
              <p className="text-sm text-slate-200 leading-relaxed">{selectedPlayer.bio}</p>

              <div className="p-3 rounded-xl bg-[#0F1A2E] border border-[#1F314F]">
                <span className="text-[11px] font-bold text-slate-400 uppercase">Key Super-Power</span>
                <p className="text-xs font-bold text-[#00F5D4] mt-0.5">{selectedPlayer.key_strength}</p>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono pt-2">
                <div className="p-2.5 rounded-lg bg-[#0F1A2E] border border-[#1F314F]">
                  <span className="text-slate-400 block text-[10px]">NORMAL MATCH SCORE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedPlayer.norm_sr || selectedPlayer.norm_econ}
                  </span>
                </div>
                <div className="p-2.5 rounded-lg bg-[#0F1A2E] border border-[#EA1A85]/30">
                  <span className="text-[#FF4DAB] block text-[10px]">HIGH-PRESSURE SCORE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedPlayer.hp_sr || selectedPlayer.hp_econ}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className="mt-16 border-t border-[#1F314F] bg-[#060B14]/90 py-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#EA1A85] animate-pulse"></span>
            <span className="font-bold text-slate-400">Rajasthan Royals SupeRR Selector • Round 1 Official Submission</span>
          </div>
          <div>
            Built with Next.js, Tailwind CSS & Python Data Science Stack
          </div>
        </div>
      </footer>

    </div>
  );
}
