const CRICKET_DATA = {
  "summary": {
    "total_deliveries": 200999,
    "total_matches": 867,
    "ipl_matches": 371,
    "t20i_matches": 482,
    "qualified_batters": 162,
    "qualified_bowlers": 243,
    "hp_threshold": 0.7,
    "hp_balls": 60314
  },
  "batters": [
    {
      "rank": 1,
      "name": "Naman Dhir",
      "team": "Mumbai Indians / Punjab",
      "role": "Finisher / Dynamic 360\u00b0 Hitter",
      "image": "players/naman_dhir.jpg",
      "bio": "Empirically the #1 clutch batter in the entire dataset. Elevates performance by +51% under extreme pressure (PPR: 1.51) with a staggering 187.5 strike rate in high-leverage death chases.",
      "key_strength": "Explosive Boundary Conversion (27.5% in HP)",
      "archetype": "Clutch Giant",
      "hp_balls": 265,
      "hp_runs": 497,
      "hp_sr": 187.5,
      "hp_avg": 31.1,
      "hp_bdry_pct": 27.5,
      "hp_rot_pct": 45.7,
      "norm_sr": 152.8,
      "norm_avg": 26.1,
      "ppr": 1.51,
      "final_score": 87.7,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 2,
      "name": "Shashank Singh",
      "team": "Punjab Kings / Chhattisgarh",
      "role": "Crisis Finisher / Pressure Absorber",
      "image": "players/shashank_singh.jpg",
      "bio": "The iceman of lower-order chases. Boasts an extraordinary 38.1 average under high pressure while striking at 167.3. Delivers a 1.13x lift in games where top order collapsed.",
      "key_strength": "High-leverage chase composure & 51.6% strike rotation",
      "archetype": "Clutch Giant",
      "hp_balls": 364,
      "hp_runs": 609,
      "hp_sr": 167.3,
      "hp_avg": 38.1,
      "hp_bdry_pct": 22.0,
      "hp_rot_pct": 51.6,
      "norm_sr": 151.0,
      "norm_avg": 37.0,
      "ppr": 1.13,
      "final_score": 84.3,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 3,
      "name": "Tim David",
      "team": "Mumbai Indians / Australia",
      "role": "Designated Death Overs Demolisher",
      "image": "players/tim_david.jpg",
      "bio": "Massive volume clutch specialist with 1,345 high-pressure runs. Boasts a 176.3 HP strike rate and 24.6% boundary rate when RRR crosses 11.5.",
      "key_strength": "Heavy power hitting against Tier-1 pace in Death",
      "archetype": "Clutch Giant",
      "hp_balls": 763,
      "hp_runs": 1345,
      "hp_sr": 176.3,
      "hp_avg": 36.4,
      "hp_bdry_pct": 24.6,
      "hp_rot_pct": 45.0,
      "norm_sr": 179.9,
      "norm_avg": 32.0,
      "ppr": 1.13,
      "final_score": 81.5,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 4,
      "name": "Namboori Tilak Varma",
      "team": "Mumbai Indians / India",
      "role": "Middle-Order Stabilizer & Finisher",
      "image": "players/tilak_varma.jpg",
      "bio": "World-class crisis anchor who elevates by +30% (PPR: 1.30) in critical playoff and decider fixtures. Accumulated 1,264 HP runs at a 39.5 average with 166.3 SR.",
      "key_strength": "Gear shifting from 30/3 rescue to death acceleration",
      "archetype": "Clutch Giant",
      "hp_balls": 760,
      "hp_runs": 1264,
      "hp_sr": 166.3,
      "hp_avg": 39.5,
      "hp_bdry_pct": 22.4,
      "hp_rot_pct": 48.9,
      "norm_sr": 132.9,
      "norm_avg": 40.9,
      "ppr": 1.3,
      "final_score": 81.1,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 5,
      "name": "Jos Buttler",
      "team": "Rajasthan Royals / England",
      "role": "Elite Opener & Match Winner",
      "image": "players/jos_buttler.jpg",
      "bio": "The gold standard of high-stakes acceleration. Strikes at 172.2 under pressure with a 26.7% boundary rate. Dominates both fortress away grounds and championship finals.",
      "key_strength": "Boundary acceleration against new-ball & death swing",
      "archetype": "Clutch Giant",
      "hp_balls": 187,
      "hp_runs": 322,
      "hp_sr": 172.2,
      "hp_avg": 35.8,
      "hp_bdry_pct": 26.7,
      "hp_rot_pct": 43.3,
      "norm_sr": 154.2,
      "norm_avg": 40.7,
      "ppr": 1.15,
      "final_score": 81.0,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 6,
      "name": "Rishabh Pant",
      "team": "Delhi Capitals / India",
      "role": "Wicketkeeper Batter / Counter-Attacker",
      "image": "players/rishabh_pant.jpg",
      "bio": "Quintessential Crisis Specialist. Massive +39% elevation under pressure (PPR: 1.39). Smashes 170.0 SR when entering at 4 wickets down, destroying opposition momentum.",
      "key_strength": "Fearless ramp & lofted boundary hitting in collapse situations",
      "archetype": "Crisis Specialist",
      "hp_balls": 277,
      "hp_runs": 471,
      "hp_sr": 170.0,
      "hp_avg": 36.2,
      "hp_bdry_pct": 24.5,
      "hp_rot_pct": 43.0,
      "norm_sr": 135.3,
      "norm_avg": 27.7,
      "ppr": 1.39,
      "final_score": 79.4,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 7,
      "name": "Matthew Wade",
      "team": "Gujarat Titans / Australia",
      "role": "Lower-Order Finisher",
      "image": "players/matthew_wade.jpg",
      "bio": "Elevates by a gargantuan +56% (PPR: 1.56) in tournament knockouts. Maintains a 41.6 average in pressure balls, famous for ice-cool scoop shots when 12+ per over is needed.",
      "key_strength": "Ramp shots vs extreme 145kph+ pace in knockouts",
      "archetype": "Crisis Specialist",
      "hp_balls": 223,
      "hp_runs": 333,
      "hp_sr": 149.3,
      "hp_avg": 41.6,
      "hp_bdry_pct": 18.4,
      "hp_rot_pct": 49.3,
      "norm_sr": 127.0,
      "norm_avg": 25.9,
      "ppr": 1.56,
      "final_score": 78.9,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 8,
      "name": "Shreyas Iyer",
      "team": "Kolkata Knight Riders / India",
      "role": "One-Down Captain & Spin Neutralizer",
      "image": "players/shreyas_iyer.jpg",
      "bio": "Championship-winning captain with a 174.5 strike rate under pressure. Exceptional at dismantling spin in high-leverage middle overs with a 51.4% strike rotation rate.",
      "key_strength": "High-pressure middle-over strike rotation (51.4%)",
      "archetype": "Clutch Giant",
      "hp_balls": 286,
      "hp_runs": 499,
      "hp_sr": 174.5,
      "hp_avg": 26.3,
      "hp_bdry_pct": 24.1,
      "hp_rot_pct": 51.4,
      "norm_sr": 149.3,
      "norm_avg": 38.6,
      "ppr": 1.12,
      "final_score": 78.8,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 9,
      "name": "Rajat Patidar",
      "team": "Royal Challengers Bengaluru / MP",
      "role": "Aggressive Spin Destroyer & Accelerator",
      "image": "players/rajat_patidar.jpg",
      "bio": "Proven playoff centurion. Strikes at 170.3 under pressure with a 23.7% boundary rate. Neutralizes both spin and high-pace bowling when match consequence is critical.",
      "key_strength": "Playoff acceleration & fearless six-hitting over mid-wicket",
      "archetype": "Clutch Giant",
      "hp_balls": 219,
      "hp_runs": 373,
      "hp_sr": 170.3,
      "hp_avg": 33.9,
      "hp_bdry_pct": 23.7,
      "hp_rot_pct": 46.6,
      "norm_sr": 167.1,
      "norm_avg": 35.4,
      "ppr": 1.01,
      "final_score": 78.5,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 10,
      "name": "Tristan Stubbs",
      "team": "Delhi Capitals / South Africa",
      "role": "360\u00b0 Finisher & Crisis Rescuer",
      "image": "players/tristan_stubbs.jpg",
      "bio": "Crossed 1,028 high-pressure runs with 158.6 SR and 35.4 average. Possesses a 1.13x pressure lift, specializing in inventive strokeplay in high RRR run chases.",
      "key_strength": "Reverse sweeps and innovative death scoring",
      "archetype": "Clutch Giant",
      "hp_balls": 648,
      "hp_runs": 1028,
      "hp_sr": 158.6,
      "hp_avg": 35.4,
      "hp_bdry_pct": 20.2,
      "hp_rot_pct": 51.9,
      "norm_sr": 136.9,
      "norm_avg": 37.1,
      "ppr": 1.13,
      "final_score": 78.0,
      "quadrant": "Quadrant 1: Clutch Giants"
    }
  ],
  "bowlers": [
    {
      "rank": 1,
      "name": "Sunil Narine",
      "team": "Kolkata Knight Riders / West Indies",
      "role": "Mystery Spinner / Death Enforcer",
      "image": "players/sunil_narine.jpg",
      "bio": "Empirically the #1 clutch bowler in modern T20 cricket. Concedes an astonishingly low 6.76 economy across 448 high-pressure balls with a 16.6 strike rate. 40.0% post-boundary comeback rate.",
      "key_strength": "Impenetrable boundary choke (11.1% boundary rate)",
      "archetype": "Clutch Giant",
      "hp_balls": 448,
      "hp_econ": 6.76,
      "hp_wsr": 16.6,
      "hp_wkts": 27,
      "post_bdry_comp": 40.0,
      "norm_econ": 6.76,
      "ppr": 1.2,
      "final_score": 76.8,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 2,
      "name": "Jasprit Bumrah",
      "team": "Mumbai Indians / India",
      "role": "All-Phase Pace Weapon & Yorker King",
      "image": "players/jasprit_bumrah.jpg",
      "bio": "The world benchmark. Bowled 736 high-pressure deliveries (highest volume) maintaining a microscopic 6.88 economy. Displays unmatched 46.8% post-boundary composure.",
      "key_strength": "Laser yorkers & 46.8% post-boundary dot/wicket comeback",
      "archetype": "Clutch Giant",
      "hp_balls": 736,
      "hp_econ": 6.88,
      "hp_wsr": 21.0,
      "hp_wkts": 35,
      "post_bdry_comp": 46.8,
      "norm_econ": 6.83,
      "ppr": 1.14,
      "final_score": 72.5,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 3,
      "name": "Shaheen Afridi",
      "team": "Pakistan / Lahore Qalandars",
      "role": "Powerplay Weapon & Inswing Specialist",
      "image": "players/shaheen_afridi.jpg",
      "bio": "Lethal early-breakthrough weapon. Boasts a 10.9 wicket strike rate and 7.39 economy in high-stakes matches, elevating by +28% (PPR: 1.28) in knockout fixtures.",
      "key_strength": "First-over knockout breakthroughs (WSR: 10.9)",
      "archetype": "Clutch Giant",
      "hp_balls": 349,
      "hp_econ": 7.39,
      "hp_wsr": 10.9,
      "hp_wkts": 32,
      "post_bdry_comp": 43.0,
      "norm_econ": 7.76,
      "ppr": 1.28,
      "final_score": 69.2,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "rank": 4,
      "name": "Faheem Ashraf",
      "team": "Islamabad United / Pakistan",
      "role": "Pace All-Rounder & Death Squeezer",
      "image": "players/faheem_ashraf.jpg",
      "bio": "Extreme Crisis Specialist (+60% elevation under pressure). Concedes only 7.57 economy in tight games with a 12.2 strike rate and 48.6% post-boundary dot/wicket rate.",
      "key_strength": "48.6% post-boundary recovery and heavy death yorkers",
      "archetype": "Crisis Specialist",
      "hp_balls": 122,
      "hp_econ": 7.57,
      "hp_wsr": 12.2,
      "hp_wkts": 10,
      "post_bdry_comp": 48.6,
      "norm_econ": 8.53,
      "ppr": 1.6,
      "final_score": 68.7,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 5,
      "name": "Riley Meredith",
      "team": "Mumbai Indians / Australia",
      "role": "High-Velocity Enforcer (145kph+)",
      "image": "players/riley_meredith.jpg",
      "bio": "Pace thunderbolt with a blistering 10.7 wicket strike rate under high pressure. Elevated his impact from normal games to crunch moments by +60% (PPR: 1.60).",
      "key_strength": "Sheer pace yorkers and 45.7% bounce-back composure",
      "archetype": "Crisis Specialist",
      "hp_balls": 139,
      "hp_econ": 8.5,
      "hp_wsr": 10.7,
      "hp_wkts": 13,
      "post_bdry_comp": 45.7,
      "norm_econ": 8.56,
      "ppr": 1.6,
      "final_score": 68.7,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 6,
      "name": "Haris Rauf",
      "team": "Pakistan / Lahore Qalandars",
      "role": "Death Overs Fast Bowler",
      "image": "players/haris_rauf.jpg",
      "bio": "High-leverage strike weapon. Across 363 HP balls, claims a wicket every 11.7 deliveries. Thrives in high-ego rivalries like IND vs PAK and tight death finishes.",
      "key_strength": "Heavy 150kph reverse yorkers and 11.7 WSR in Death",
      "archetype": "Crisis Specialist",
      "hp_balls": 363,
      "hp_econ": 7.92,
      "hp_wsr": 11.7,
      "hp_wkts": 31,
      "post_bdry_comp": 38.1,
      "norm_econ": 8.62,
      "ppr": 1.39,
      "final_score": 67.5,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 7,
      "name": "Alzarri Joseph",
      "team": "Gujarat Titans / West Indies",
      "role": "Hit-the-Deck Fast Bowler",
      "image": "players/alzarri_joseph.jpg",
      "bio": "Bowled 458 high-pressure balls with a 15.3 strike rate and 42.5% post-boundary composure. Unlocks aggressive bounce on hostile away pitches.",
      "key_strength": "Steep bounce and 15.3 WSR in middle/death overs",
      "archetype": "Crisis Specialist",
      "hp_balls": 458,
      "hp_econ": 8.66,
      "hp_wsr": 15.3,
      "hp_wkts": 30,
      "post_bdry_comp": 42.5,
      "norm_econ": 9.61,
      "ppr": 1.6,
      "final_score": 66.1,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 8,
      "name": "Shadab Khan",
      "team": "Islamabad United / Pakistan",
      "role": "Leg-Spin All-Rounder & Middle Choker",
      "image": "players/shadab_khan.jpg",
      "bio": "Elite spin control. Holds an unbelievable 6.72 economy under pressure with +57% elevation (PPR: 1.57), suffocating opposition batters in playoff middle overs.",
      "key_strength": "Tight 6.72 economy and deceptive wrong-un in crisis",
      "archetype": "Crisis Specialist",
      "hp_balls": 125,
      "hp_econ": 6.72,
      "hp_wsr": 20.8,
      "hp_wkts": 6,
      "post_bdry_comp": 30.0,
      "norm_econ": 7.93,
      "ppr": 1.57,
      "final_score": 64.8,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 9,
      "name": "Xavier Bartlett",
      "team": "Australia / Brisbane Heat",
      "role": "Swing & Seam Wicket Taker",
      "image": "players/xavier_bartlett.jpg",
      "bio": "Breakout clutch performer (+60% elevation). Takes 13 wickets in 241 HP balls with an 18.5 strike rate and 41.3% post-boundary comeback rate.",
      "key_strength": "Late outswing in powerplay and 41.3% composure",
      "archetype": "Crisis Specialist",
      "hp_balls": 241,
      "hp_econ": 8.61,
      "hp_wsr": 18.5,
      "hp_wkts": 13,
      "post_bdry_comp": 41.3,
      "norm_econ": 9.26,
      "ppr": 1.6,
      "final_score": 64.4,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "rank": 10,
      "name": "Axar Patel",
      "team": "Delhi Capitals / India",
      "role": "Defensive Left-Arm Spinner & Finisher",
      "image": "players/axar_patel.jpg",
      "bio": "Massive volume clutch bowler (603 HP deliveries). Concedes just 7.58 RPO with 33 wickets (WSR: 18.3). Iconic performer in T20 World Cup 2024 final under extreme pressure.",
      "key_strength": "Flat, darting trajectory that denies room in crunch overs",
      "archetype": "Clutch Giant",
      "hp_balls": 603,
      "hp_econ": 7.58,
      "hp_wsr": 18.3,
      "hp_wkts": 33,
      "post_bdry_comp": 36.8,
      "norm_econ": 7.83,
      "ppr": 1.23,
      "final_score": 64.2,
      "quadrant": "Quadrant 1: Clutch Giants"
    }
  ],
  "pressure_proof_xi": {
    "batting_lineup": [
      {
        "slot": 1,
        "role": "Opener / Aggressor",
        "name": "Virat Kohli",
        "team": "Royal Challengers Bengaluru / India",
        "image": "players/virat_kohli.jpg",
        "hp_sr": 197.4,
        "hp_avg": 38.5,
        "score": 68.4,
        "desc": "T20 World Cup 2024 Final hero. Unprecedented 197.4 strike rate when opening under immediate tournament pressure."
      },
      {
        "slot": 2,
        "role": "Opener / Wicketkeeper",
        "name": "Quinton de Kock",
        "team": "Lucknow Super Giants / South Africa",
        "image": "players/quinton_de_kock.jpg",
        "hp_sr": 152.4,
        "hp_avg": 48.0,
        "score": 76.8,
        "desc": "Calm, explosive wicketkeeper-opener averaging 48.0 against Tier-1 pace attacks in critical Powerplays."
      },
      {
        "slot": 3,
        "role": "One-Down / Captain & Anchor",
        "name": "Shreyas Iyer",
        "team": "Kolkata Knight Riders / India",
        "image": "players/shreyas_iyer.jpg",
        "hp_sr": 198.3,
        "hp_avg": 58.5,
        "score": 85.3,
        "desc": "Astonishing 58.5 average and 198.3 strike rate at Position 3 under pressure. The definitive anchor-destroyer."
      },
      {
        "slot": 4,
        "role": "Middle Power / Acceleration",
        "name": "Rovman Powell",
        "team": "Rajasthan Royals / West Indies",
        "image": "players/rovman_powell.jpg",
        "hp_sr": 170.0,
        "hp_avg": 39.7,
        "score": 91.9,
        "desc": "RR powerhouse captain. Unmatched 91.9 clutch rating at slot 4, punishing spinners and death pacers alike."
      },
      {
        "slot": 5,
        "role": "Crisis Stabilizer & Counter-Attacker",
        "name": "Namboori Tilak Varma",
        "team": "Mumbai Indians / India",
        "image": "players/tilak_varma.jpg",
        "hp_sr": 168.5,
        "hp_avg": 45.3,
        "score": 89.0,
        "desc": "Rescues innings from collapses. 679 pressure runs at 45.3 average and 168.5 SR in high-stakes middle overs."
      },
      {
        "slot": 6,
        "role": "Death Finisher / Ice-Man",
        "name": "Shashank Singh",
        "team": "Punjab Kings",
        "image": "players/shashank_singh.jpg",
        "hp_sr": 164.9,
        "hp_avg": 45.0,
        "score": 89.6,
        "desc": "Dead-eye finisher averaging 45.0 when chasing 12+ RRR with ice-cool boundary execution."
      },
      {
        "slot": 7,
        "role": "Lower Clutch Demolisher",
        "name": "Naman Dhir",
        "team": "Mumbai Indians",
        "image": "players/naman_dhir.jpg",
        "hp_sr": 197.0,
        "hp_avg": 43.7,
        "score": 97.2,
        "desc": "Highest position score in tournament (97.2). Strikes at 197.0 in death overs with a 27.5% boundary conversion rate."
      }
    ],
    "bowling_attack": [
      {
        "role": "Powerplay Weapon",
        "name": "Shaheen Afridi",
        "team": "Pakistan",
        "image": "players/shaheen_afridi.jpg",
        "hp_econ": 6.19,
        "hp_wsr": 14.2,
        "post_b_comp": 55.1,
        "score": 82.5,
        "desc": "Concedes just 6.19 in high-pressure Powerplays with an incredible 55.1% post-boundary comeback rate."
      },
      {
        "role": "Middle Squeezer",
        "name": "Harpreet Brar",
        "team": "Punjab Kings",
        "image": "players/harpreet_brar.jpg",
        "hp_econ": 6.35,
        "hp_wsr": 13.9,
        "post_b_comp": 30.0,
        "score": 79.7,
        "desc": "Suffocates the opposition in overs 7-15, boasting a 6.35 economy and 13.9 strike rate in pressure games."
      },
      {
        "role": "Death Yorker Specialist",
        "name": "Jasprit Bumrah",
        "team": "Mumbai Indians / India",
        "image": "players/jasprit_bumrah.jpg",
        "hp_econ": 6.88,
        "hp_wsr": 21.0,
        "post_b_comp": 46.8,
        "score": 72.5,
        "desc": "Global #1 death bowler. 736 HP deliveries with 46.8% post-boundary composure and lethal pinpoint yorkers."
      },
      {
        "role": "Death Enforcer & Spinner",
        "name": "Sunil Narine",
        "team": "Kolkata Knight Riders",
        "image": "players/sunil_narine.jpg",
        "hp_econ": 6.18,
        "hp_wsr": 11.2,
        "post_b_comp": 43.8,
        "score": 89.7,
        "desc": "Tournament #1 clutch bowler. 6.18 economy at the death, giving up virtually zero boundaries (11.1%)."
      }
    ]
  },
  "scatter_batters": [
    {
      "name": "Naman Dhir",
      "norm_score": 60.9,
      "hp_score": 91.8,
      "ppr": 1.51,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Shashank Singh",
      "norm_score": 82.7,
      "hp_score": 93.5,
      "ppr": 1.13,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Tim David",
      "norm_score": 79.3,
      "hp_score": 89.8,
      "ppr": 1.13,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Namboori Tilak Varma",
      "norm_score": 66.6,
      "hp_score": 86.5,
      "ppr": 1.3,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Jos Buttler",
      "norm_score": 76.9,
      "hp_score": 88.7,
      "ppr": 1.15,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Rishabh Pant",
      "norm_score": 59.5,
      "hp_score": 82.7,
      "ppr": 1.39,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Matthew Wade",
      "norm_score": 50.6,
      "hp_score": 79.1,
      "ppr": 1.56,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Shreyas Iyer",
      "norm_score": 77.3,
      "hp_score": 86.4,
      "ppr": 1.12,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Rajat Patidar",
      "norm_score": 87.1,
      "hp_score": 87.9,
      "ppr": 1.01,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Tristan Stubbs",
      "norm_score": 75.2,
      "hp_score": 85.1,
      "ppr": 1.13,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Heinrich Klaasen",
      "norm_score": 98.8,
      "hp_score": 88.8,
      "ppr": 0.9,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Cameron Green",
      "norm_score": 72.5,
      "hp_score": 83.0,
      "ppr": 1.14,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Marcus Stoinis",
      "norm_score": 64.0,
      "hp_score": 80.1,
      "ppr": 1.25,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "David Miller",
      "norm_score": 78.5,
      "hp_score": 82.8,
      "ppr": 1.05,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Vijay Shankar",
      "norm_score": 57.8,
      "hp_score": 75.8,
      "ppr": 1.31,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Rinku Singh",
      "norm_score": 73.4,
      "hp_score": 78.3,
      "ppr": 1.07,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Ravindra Jadeja",
      "norm_score": 63.7,
      "hp_score": 74.1,
      "ppr": 1.16,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Daryl Mitchell",
      "norm_score": 64.7,
      "hp_score": 74.4,
      "ppr": 1.15,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Sanju Samson",
      "norm_score": 67.5,
      "hp_score": 75.0,
      "ppr": 1.11,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Rassie van der Dussen",
      "norm_score": 34.2,
      "hp_score": 77.1,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Sikandar Raza",
      "norm_score": 41.4,
      "hp_score": 66.5,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Dhruv Jurel",
      "norm_score": 73.1,
      "hp_score": 75.7,
      "ppr": 1.03,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Dinesh Karthik",
      "norm_score": 86.6,
      "hp_score": 77.7,
      "ppr": 0.9,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Shadab Khan",
      "norm_score": 40.9,
      "hp_score": 65.8,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Suryakumar Yadav",
      "norm_score": 81.2,
      "hp_score": 76.3,
      "ppr": 0.94,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Romario Shepherd",
      "norm_score": 33.5,
      "hp_score": 65.0,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Nicholas Pooran",
      "norm_score": 72.8,
      "hp_score": 73.3,
      "ppr": 1.01,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Shivam Dube",
      "norm_score": 76.7,
      "hp_score": 73.7,
      "ppr": 0.96,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Hardik Pandya",
      "norm_score": 62.6,
      "hp_score": 69.2,
      "ppr": 1.11,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Towhid Hridoy",
      "norm_score": 45.2,
      "hp_score": 63.6,
      "ppr": 1.41,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Anuj Rawat",
      "norm_score": 29.0,
      "hp_score": 63.4,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Donovan Ferreira",
      "norm_score": 66.7,
      "hp_score": 69.3,
      "ppr": 1.04,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Glenn Phillips",
      "norm_score": 76.0,
      "hp_score": 70.8,
      "ppr": 0.93,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Iftikhar Ahmed",
      "norm_score": 45.9,
      "hp_score": 62.9,
      "ppr": 1.37,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Moeen Ali",
      "norm_score": 53.1,
      "hp_score": 65.1,
      "ppr": 1.23,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Ravichandran Ashwin",
      "norm_score": 46.3,
      "hp_score": 62.8,
      "ppr": 1.36,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Nitish Reddy",
      "norm_score": 73.8,
      "hp_score": 69.1,
      "ppr": 0.94,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Ayush Badoni",
      "norm_score": 64.8,
      "hp_score": 66.4,
      "ppr": 1.02,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Lokesh Rahul",
      "norm_score": 78.3,
      "hp_score": 68.8,
      "ppr": 0.88,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Venkatesh Iyer",
      "norm_score": 68.5,
      "hp_score": 66.5,
      "ppr": 0.97,
      "quadrant": "Quadrant 1: Clutch Giants"
    }
  ],
  "scatter_bowlers": [
    {
      "name": "Sunil Narine",
      "norm_score": 68.9,
      "hp_score": 82.5,
      "ppr": 1.2,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Jasprit Bumrah",
      "norm_score": 68.0,
      "hp_score": 77.6,
      "ppr": 1.14,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Shaheen Afridi",
      "norm_score": 55.5,
      "hp_score": 70.9,
      "ppr": 1.28,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Faheem Ashraf",
      "norm_score": 39.7,
      "hp_score": 74.9,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Riley Meredith",
      "norm_score": 29.9,
      "hp_score": 68.5,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Haris Rauf",
      "norm_score": 48.2,
      "hp_score": 66.9,
      "ppr": 1.39,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Alzarri Joseph",
      "norm_score": 35.9,
      "hp_score": 61.5,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Shadab Khan",
      "norm_score": 43.8,
      "hp_score": 68.6,
      "ppr": 1.57,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Xavier Bartlett",
      "norm_score": 33.8,
      "hp_score": 59.2,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Axar Patel",
      "norm_score": 53.2,
      "hp_score": 65.2,
      "ppr": 1.23,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Abrar Ahmed",
      "norm_score": 63.9,
      "hp_score": 67.8,
      "ppr": 1.06,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Moeen Ali",
      "norm_score": 53.3,
      "hp_score": 64.6,
      "ppr": 1.21,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Mohammad Nawaz",
      "norm_score": 58.3,
      "hp_score": 65.9,
      "ppr": 1.13,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Kuldeep Yadav",
      "norm_score": 61.3,
      "hp_score": 65.5,
      "ppr": 1.07,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Harpreet Brar",
      "norm_score": 53.3,
      "hp_score": 61.1,
      "ppr": 1.15,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Jason Behrendorff",
      "norm_score": 53.8,
      "hp_score": 60.7,
      "ppr": 1.13,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Maheesh Theekshana",
      "norm_score": 47.6,
      "hp_score": 58.8,
      "ppr": 1.24,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Ravi Bishnoi",
      "norm_score": 51.1,
      "hp_score": 59.6,
      "ppr": 1.17,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Nandre Burger",
      "norm_score": 35.6,
      "hp_score": 52.8,
      "ppr": 1.48,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Lungi Ngidi",
      "norm_score": 58.3,
      "hp_score": 59.5,
      "ppr": 1.02,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Noor Ahmad",
      "norm_score": 64.0,
      "hp_score": 60.0,
      "ppr": 0.94,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Sikandar Raza",
      "norm_score": 49.8,
      "hp_score": 56.5,
      "ppr": 1.13,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Taskin Ahmed",
      "norm_score": 54.0,
      "hp_score": 57.5,
      "ppr": 1.07,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Trent Boult",
      "norm_score": 55.3,
      "hp_score": 57.6,
      "ppr": 1.04,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Bhuvneshwar Kumar",
      "norm_score": 59.1,
      "hp_score": 58.3,
      "ppr": 0.99,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Murugan Ashwin",
      "norm_score": 25.4,
      "hp_score": 76.0,
      "ppr": 1.6,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Odean Smith",
      "norm_score": 36.2,
      "hp_score": 50.9,
      "ppr": 1.41,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Akeal Hosein",
      "norm_score": 58.4,
      "hp_score": 57.0,
      "ppr": 0.98,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Mitchell Santner",
      "norm_score": 62.4,
      "hp_score": 57.5,
      "ppr": 0.92,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Rashid Khan",
      "norm_score": 60.7,
      "hp_score": 56.6,
      "ppr": 0.93,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Spencer Johnson",
      "norm_score": 42.0,
      "hp_score": 54.0,
      "ppr": 1.28,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Varun Chakravarthy",
      "norm_score": 68.8,
      "hp_score": 57.5,
      "ppr": 0.84,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Wanindu Hasaranga",
      "norm_score": 59.8,
      "hp_score": 55.5,
      "ppr": 0.93,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Matheesha Pathirana",
      "norm_score": 70.3,
      "hp_score": 57.1,
      "ppr": 0.81,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Tim Southee",
      "norm_score": 53.4,
      "hp_score": 53.1,
      "ppr": 0.99,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Kagiso Rabada",
      "norm_score": 51.0,
      "hp_score": 52.1,
      "ppr": 1.02,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Allah Ghazanfar",
      "norm_score": 48.5,
      "hp_score": 53.9,
      "ppr": 1.11,
      "quadrant": "Quadrant 2: Crisis Specialists"
    },
    {
      "name": "Corbin Bosch",
      "norm_score": 71.3,
      "hp_score": 60.3,
      "ppr": 0.85,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Nathan Ellis",
      "norm_score": 62.2,
      "hp_score": 54.4,
      "ppr": 0.87,
      "quadrant": "Quadrant 1: Clutch Giants"
    },
    {
      "name": "Glenn Maxwell",
      "norm_score": 46.9,
      "hp_score": 50.7,
      "ppr": 1.08,
      "quadrant": "Quadrant 2: Crisis Specialists"
    }
  ]
};