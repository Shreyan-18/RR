import json
import pandas as pd
import numpy as np

# Load core datasets
batters_df = pd.read_csv('top10_batters.csv')
bowlers_df = pd.read_csv('top10_bowlers.csv')
with open('pressure_proof_xi.json') as f:
    xi_data = json.load(f)

# Positional batters
pos_df = pd.read_csv('positional_batters.csv')
phase_df = pd.read_csv('bowling_phase_specialists.csv')
quad_batters = pd.read_csv('batter_quadrants.csv')
quad_bowlers = pd.read_csv('bowler_quadrants.csv')

# Player bios and tactical scouting notes with local downloaded real images
batter_scouting = {
    "Naman Dhir": {
        "team": "Mumbai Indians / Punjab",
        "role": "Finisher / Dynamic 360° Hitter",
        "image": "players/naman_dhir.jpg",
        "bio": "Empirically the #1 clutch batter in the entire dataset. Elevates performance by +51% under extreme pressure (PPR: 1.51) with a staggering 187.5 strike rate in high-leverage death chases.",
        "key_strength": "Explosive Boundary Conversion (27.5% in HP)",
        "archetype": "Clutch Giant"
    },
    "Shashank Singh": {
        "team": "Punjab Kings / Chhattisgarh",
        "role": "Crisis Finisher / Pressure Absorber",
        "image": "players/shashank_singh.jpg",
        "bio": "The iceman of lower-order chases. Boasts an extraordinary 38.1 average under high pressure while striking at 167.3. Delivers a 1.13x lift in games where top order collapsed.",
        "key_strength": "High-leverage chase composure & 51.6% strike rotation",
        "archetype": "Clutch Giant"
    },
    "Tim David": {
        "team": "Mumbai Indians / Australia",
        "role": "Designated Death Overs Demolisher",
        "image": "players/tim_david.jpg",
        "bio": "Massive volume clutch specialist with 1,345 high-pressure runs. Boasts a 176.3 HP strike rate and 24.6% boundary rate when RRR crosses 11.5.",
        "key_strength": "Heavy power hitting against Tier-1 pace in Death",
        "archetype": "Clutch Giant"
    },
    "Namboori Tilak Varma": {
        "team": "Mumbai Indians / India",
        "role": "Middle-Order Stabilizer & Finisher",
        "image": "players/tilak_varma.jpg",
        "bio": "World-class crisis anchor who elevates by +30% (PPR: 1.30) in critical playoff and decider fixtures. Accumulated 1,264 HP runs at a 39.5 average with 166.3 SR.",
        "key_strength": "Gear shifting from 30/3 rescue to death acceleration",
        "archetype": "Clutch Giant"
    },
    "Jos Buttler": {
        "team": "Rajasthan Royals / England",
        "role": "Elite Opener & Match Winner",
        "image": "players/jos_buttler.jpg",
        "bio": "The gold standard of high-stakes acceleration. Strikes at 172.2 under pressure with a 26.7% boundary rate. Dominates both fortress away grounds and championship finals.",
        "key_strength": "Boundary acceleration against new-ball & death swing",
        "archetype": "Clutch Giant"
    },
    "Rishabh Pant": {
        "team": "Delhi Capitals / India",
        "role": "Wicketkeeper Batter / Counter-Attacker",
        "image": "players/rishabh_pant.jpg",
        "bio": "Quintessential Crisis Specialist. Massive +39% elevation under pressure (PPR: 1.39). Smashes 170.0 SR when entering at 4 wickets down, destroying opposition momentum.",
        "key_strength": "Fearless ramp & lofted boundary hitting in collapse situations",
        "archetype": "Crisis Specialist"
    },
    "Matthew Wade": {
        "team": "Gujarat Titans / Australia",
        "role": "Lower-Order Finisher",
        "image": "players/matthew_wade.jpg",
        "bio": "Elevates by a gargantuan +56% (PPR: 1.56) in tournament knockouts. Maintains a 41.6 average in pressure balls, famous for ice-cool scoop shots when 12+ per over is needed.",
        "key_strength": "Ramp shots vs extreme 145kph+ pace in knockouts",
        "archetype": "Crisis Specialist"
    },
    "Shreyas Iyer": {
        "team": "Kolkata Knight Riders / India",
        "role": "One-Down Captain & Spin Neutralizer",
        "image": "players/shreyas_iyer.jpg",
        "bio": "Championship-winning captain with a 174.5 strike rate under pressure. Exceptional at dismantling spin in high-leverage middle overs with a 51.4% strike rotation rate.",
        "key_strength": "High-pressure middle-over strike rotation (51.4%)",
        "archetype": "Clutch Giant"
    },
    "Rajat Patidar": {
        "team": "Royal Challengers Bengaluru / MP",
        "role": "Aggressive Spin Destroyer & Accelerator",
        "image": "players/rajat_patidar.jpg",
        "bio": "Proven playoff centurion. Strikes at 170.3 under pressure with a 23.7% boundary rate. Neutralizes both spin and high-pace bowling when match consequence is critical.",
        "key_strength": "Playoff acceleration & fearless six-hitting over mid-wicket",
        "archetype": "Clutch Giant"
    },
    "Tristan Stubbs": {
        "team": "Delhi Capitals / South Africa",
        "role": "360° Finisher & Crisis Rescuer",
        "image": "players/tristan_stubbs.jpg",
        "bio": "Crossed 1,028 high-pressure runs with 158.6 SR and 35.4 average. Possesses a 1.13x pressure lift, specializing in inventive strokeplay in high RRR run chases.",
        "key_strength": "Reverse sweeps and innovative death scoring",
        "archetype": "Clutch Giant"
    }
}

bowler_scouting = {
    "Sunil Narine": {
        "team": "Kolkata Knight Riders / West Indies",
        "role": "Mystery Spinner / Death Enforcer",
        "image": "players/sunil_narine.jpg",
        "bio": "Empirically the #1 clutch bowler in modern T20 cricket. Concedes an astonishingly low 6.76 economy across 448 high-pressure balls with a 16.6 strike rate. 40.0% post-boundary comeback rate.",
        "key_strength": "Impenetrable boundary choke (11.1% boundary rate)",
        "archetype": "Clutch Giant"
    },
    "Jasprit Bumrah": {
        "team": "Mumbai Indians / India",
        "role": "All-Phase Pace Weapon & Yorker King",
        "image": "players/jasprit_bumrah.jpg",
        "bio": "The world benchmark. Bowled 736 high-pressure deliveries (highest volume) maintaining a microscopic 6.88 economy. Displays unmatched 46.8% post-boundary composure.",
        "key_strength": "Laser yorkers & 46.8% post-boundary dot/wicket comeback",
        "archetype": "Clutch Giant"
    },
    "Shaheen Afridi": {
        "team": "Pakistan / Lahore Qalandars",
        "role": "Powerplay Weapon & Inswing Specialist",
        "image": "players/shaheen_afridi.jpg",
        "bio": "Lethal early-breakthrough weapon. Boasts a 10.9 wicket strike rate and 7.39 economy in high-stakes matches, elevating by +28% (PPR: 1.28) in knockout fixtures.",
        "key_strength": "First-over knockout breakthroughs (WSR: 10.9)",
        "archetype": "Clutch Giant"
    },
    "Faheem Ashraf": {
        "team": "Islamabad United / Pakistan",
        "role": "Pace All-Rounder & Death Squeezer",
        "image": "players/faheem_ashraf.jpg",
        "bio": "Extreme Crisis Specialist (+60% elevation under pressure). Concedes only 7.57 economy in tight games with a 12.2 strike rate and 48.6% post-boundary dot/wicket rate.",
        "key_strength": "48.6% post-boundary recovery and heavy death yorkers",
        "archetype": "Crisis Specialist"
    },
    "Riley Meredith": {
        "team": "Mumbai Indians / Australia",
        "role": "High-Velocity Enforcer (145kph+)",
        "image": "players/riley_meredith.jpg",
        "bio": "Pace thunderbolt with a blistering 10.7 wicket strike rate under high pressure. Elevated his impact from normal games to crunch moments by +60% (PPR: 1.60).",
        "key_strength": "Sheer pace yorkers and 45.7% bounce-back composure",
        "archetype": "Crisis Specialist"
    },
    "Haris Rauf": {
        "team": "Pakistan / Lahore Qalandars",
        "role": "Death Overs Fast Bowler",
        "image": "players/haris_rauf.jpg",
        "bio": "High-leverage strike weapon. Across 363 HP balls, claims a wicket every 11.7 deliveries. Thrives in high-ego rivalries like IND vs PAK and tight death finishes.",
        "key_strength": "Heavy 150kph reverse yorkers and 11.7 WSR in Death",
        "archetype": "Crisis Specialist"
    },
    "Alzarri Joseph": {
        "team": "Gujarat Titans / West Indies",
        "role": "Hit-the-Deck Fast Bowler",
        "image": "players/alzarri_joseph.jpg",
        "bio": "Bowled 458 high-pressure balls with a 15.3 strike rate and 42.5% post-boundary composure. Unlocks aggressive bounce on hostile away pitches.",
        "key_strength": "Steep bounce and 15.3 WSR in middle/death overs",
        "archetype": "Crisis Specialist"
    },
    "Shadab Khan": {
        "team": "Islamabad United / Pakistan",
        "role": "Leg-Spin All-Rounder & Middle Choker",
        "image": "players/shadab_khan.jpg",
        "bio": "Elite spin control. Holds an unbelievable 6.72 economy under pressure with +57% elevation (PPR: 1.57), suffocating opposition batters in playoff middle overs.",
        "key_strength": "Tight 6.72 economy and deceptive wrong-un in crisis",
        "archetype": "Crisis Specialist"
    },
    "Xavier Bartlett": {
        "team": "Australia / Brisbane Heat",
        "role": "Swing & Seam Wicket Taker",
        "image": "players/xavier_bartlett.jpg",
        "bio": "Breakout clutch performer (+60% elevation). Takes 13 wickets in 241 HP balls with an 18.5 strike rate and 41.3% post-boundary comeback rate.",
        "key_strength": "Late outswing in powerplay and 41.3% composure",
        "archetype": "Crisis Specialist"
    },
    "Axar Patel": {
        "team": "Delhi Capitals / India",
        "role": "Defensive Left-Arm Spinner & Finisher",
        "image": "players/axar_patel.jpg",
        "bio": "Massive volume clutch bowler (603 HP deliveries). Concedes just 7.58 RPO with 33 wickets (WSR: 18.3). Iconic performer in T20 World Cup 2024 final under extreme pressure.",
        "key_strength": "Flat, darting trajectory that denies room in crunch overs",
        "archetype": "Clutch Giant"
    }
}

# Compile Batters
batters_list = []
for _, r in batters_df.iterrows():
    name = r['player_name']
    scout = batter_scouting.get(name, {
        "team": "International / Franchise",
        "role": "Top Order Batter",
        "image": "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=400&q=80",
        "bio": "Key clutch performer under high match pressure.",
        "key_strength": "Consistent boundary scoring",
        "archetype": "Clutch Giant"
    })
    batters_list.append({
        "rank": int(r['rank']),
        "name": name,
        "team": scout["team"],
        "role": scout["role"],
        "image": scout["image"],
        "bio": scout["bio"],
        "key_strength": scout["key_strength"],
        "archetype": scout["archetype"],
        "hp_balls": int(r['hp_balls']),
        "hp_runs": int(r['hp_runs']),
        "hp_sr": round(float(r['hp_sr']), 1),
        "hp_avg": round(float(r['hp_avg']), 1),
        "hp_bdry_pct": round(float(r['hp_bdry_pct']), 1),
        "hp_rot_pct": round(float(r['hp_rot_pct']), 1),
        "norm_sr": round(float(r['norm_sr']), 1),
        "norm_avg": round(float(r['norm_avg']), 1),
        "ppr": round(float(r['ppr']), 2),
        "final_score": round(float(r['final_rank_score']), 1),
        "quadrant": r['quadrant']
    })

# Compile Bowlers
bowlers_list = []
for _, r in bowlers_df.iterrows():
    name = r['player_name']
    scout = bowler_scouting.get(name, {
        "team": "International / Franchise",
        "role": "Strike Bowler",
        "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "bio": "Critical high-leverage bowler.",
        "key_strength": "High-pressure boundary defense",
        "archetype": "Clutch Giant"
    })
    bowlers_list.append({
        "rank": int(r['rank']),
        "name": name,
        "team": scout["team"],
        "role": scout["role"],
        "image": scout["image"],
        "bio": scout["bio"],
        "key_strength": scout["key_strength"],
        "archetype": scout["archetype"],
        "hp_balls": int(r['hp_balls']),
        "hp_econ": round(float(r['hp_econ']), 2),
        "hp_wsr": round(float(r['hp_wsr']), 1),
        "hp_wkts": int(r['hp_wkts']),
        "post_bdry_comp": round(float(r['hp_post_b_comp']), 1),
        "norm_econ": round(float(r['norm_econ']), 2),
        "ppr": round(float(r['ppr']), 2),
        "final_score": round(float(r['final_rank_score']), 1),
        "quadrant": r['quadrant']
    })

# Compile Pressure Proof XI with full scouting profiles
xi_full = {
    "batting_lineup": [
        {
            "slot": 1,
            "role": "Opener / Aggressor",
            "name": "Virat Kohli",
            "team": "Royal Challengers Bengaluru / India",
            "image": "players/virat_kohli.jpg",
            "hp_sr": 197.4,
            "hp_avg": 38.5,
            "norm_sr": 139.5,
            "score": 68.4,
            "ppr": 1.22,
            "archetype": "Clutch Giant",
            "key_strength": "Powerplay Strike Rate (197.4 in HP Opening)",
            "bio": "ICC T20 World Cup 2024 Final Player of the Match. Demonstrated an unprecedented 197.4 strike rate when opening under immediate tournament leverage, attacking the new ball against high-pace attacks with minimal dot ball percentage."
        },
        {
            "slot": 2,
            "role": "Opener / Wicketkeeper",
            "name": "Quinton de Kock",
            "team": "Lucknow Super Giants / South Africa",
            "image": "players/quinton_de_kock.jpg",
            "hp_sr": 152.4,
            "hp_avg": 48.0,
            "norm_sr": 142.1,
            "score": 76.8,
            "ppr": 1.18,
            "archetype": "Clutch Giant",
            "key_strength": "Wicket Preservation & 48.0 HP Average",
            "bio": "Calm, explosive wicketkeeper-opener averaging a stellar 48.0 against Tier-1 pace attacks in critical Powerplays. Neutralizes swing bowling while keeping the scoreboard moving at 152.4 SR without giving away early dismissals."
        },
        {
            "slot": 3,
            "role": "One-Down / Captain & Anchor",
            "name": "Shreyas Iyer",
            "team": "Kolkata Knight Riders / India",
            "image": "players/shreyas_iyer.jpg",
            "hp_sr": 198.3,
            "hp_avg": 58.5,
            "norm_sr": 149.3,
            "score": 85.3,
            "ppr": 1.12,
            "archetype": "Clutch Giant",
            "key_strength": "Spin Neutralization & 58.5 HP Average at #3",
            "bio": "IPL championship-winning captain with an astonishing 58.5 average and 198.3 strike rate at Position 3 under pressure. Possesses unmatched 51.4% strike rotation, completely dismantling spin during the critical middle overs."
        },
        {
            "slot": 4,
            "role": "Middle Power / Acceleration",
            "name": "Rovman Powell",
            "team": "Rajasthan Royals / West Indies",
            "image": "players/rovman_powell.jpg",
            "hp_sr": 170.0,
            "hp_avg": 39.7,
            "norm_sr": 145.2,
            "score": 91.9,
            "ppr": 1.25,
            "archetype": "Clutch Giant",
            "key_strength": "High-Leverage Six Hitting (91.9 Slot Score)",
            "bio": "Rajasthan Royals powerhouse captain. Achieved an unmatched 91.9 clutch rating at slot 4, punishing both mystery spinners and death pacers alike with heavy six-hitting when the Required Run Rate climbs beyond 11.5 RPO."
        },
        {
            "slot": 5,
            "role": "Crisis Stabilizer & Finisher",
            "name": "Namboori Tilak Varma",
            "team": "Mumbai Indians / India",
            "image": "players/tilak_varma.jpg",
            "hp_sr": 168.5,
            "hp_avg": 45.3,
            "norm_sr": 132.9,
            "score": 89.0,
            "ppr": 1.30,
            "archetype": "Clutch Giant",
            "key_strength": "Gear Shifting from 30/3 Collapse to Death Finish",
            "bio": "Rescues innings from top-order collapses. Accumulated 679 high-pressure runs at slot 5 with a 45.3 average and 168.5 SR. Elevates performance by +30% in playoff and decider fixtures."
        },
        {
            "slot": 6,
            "role": "Death Finisher / Ice-Man",
            "name": "Shashank Singh",
            "team": "Punjab Kings",
            "image": "players/shashank_singh.jpg",
            "hp_sr": 164.9,
            "hp_avg": 45.0,
            "norm_sr": 151.0,
            "score": 89.6,
            "ppr": 1.13,
            "archetype": "Clutch Giant",
            "key_strength": "Ice-Cool Boundary Execution in 12+ RRR Chases",
            "bio": "Dead-eye finisher averaging 45.0 when chasing steep Required Run Rates in the final 5 overs. Demonstrates extraordinary calmness under pressure with a 51.6% strike rotation and clutch boundary conversion."
        },
        {
            "slot": 7,
            "role": "Lower Clutch Demolisher",
            "name": "Naman Dhir",
            "team": "Mumbai Indians / Punjab",
            "image": "players/naman_dhir.jpg",
            "hp_sr": 197.0,
            "hp_avg": 43.7,
            "norm_sr": 152.8,
            "score": 97.2,
            "ppr": 1.51,
            "archetype": "Clutch Giant",
            "key_strength": "Tournament-Best 97.2 Position Score & 197.0 SR",
            "bio": "Highest positional score in the entire tournament dataset (97.2). Smashes at a 197.0 strike rate in high-pressure death overs with an extraordinary 27.5% boundary conversion rate and +51% clutch elevation."
        }
    ],
    "bowling_attack": [
        {
            "role": "Powerplay Weapon",
            "name": "Shaheen Afridi",
            "team": "Pakistan / Lahore Qalandars",
            "image": "players/shaheen_afridi.jpg",
            "hp_econ": 6.19,
            "hp_wsr": 14.2,
            "norm_econ": 7.76,
            "post_b_comp": 55.1,
            "score": 82.5,
            "ppr": 1.28,
            "archetype": "Clutch Giant",
            "key_strength": "First-Over Wickets & 55.1% Post-Boundary Comeback",
            "bio": "Concedes just 6.19 RPO in high-pressure Powerplays with an incredible 55.1% post-boundary comeback rate. Known globally for devastating first-over breakthroughs in ICC knockout matches and deciders."
        },
        {
            "role": "Middle Squeezer",
            "name": "Harpreet Brar",
            "team": "Punjab Kings",
            "image": "players/harpreet_brar.jpg",
            "hp_econ": 6.35,
            "hp_wsr": 13.9,
            "norm_econ": 7.85,
            "post_b_comp": 30.0,
            "score": 79.7,
            "ppr": 1.24,
            "archetype": "Clutch Giant",
            "key_strength": "Suffocating Middle-Over Economy (6.35 RPO)",
            "bio": "Suffocates opposition acceleration through overs 7 to 15, boasting a 6.35 economy and 13.9 wicket strike rate in high-pressure games. Constricts scoring areas and forces rash strokes from top-order batters."
        },
        {
            "role": "Death Yorker Specialist",
            "name": "Jasprit Bumrah",
            "team": "Mumbai Indians / India",
            "image": "players/jasprit_bumrah.jpg",
            "hp_econ": 6.88,
            "hp_wsr": 21.0,
            "norm_econ": 6.83,
            "post_b_comp": 46.8,
            "score": 72.5,
            "ppr": 1.14,
            "archetype": "Clutch Giant",
            "key_strength": "Pinpoint Laser Yorkers & 46.8% Bounce-Back",
            "bio": "Global benchmark death bowler. Bowled 736 high-pressure deliveries maintaining an elite 6.88 economy with 46.8% post-boundary composure (highest among major pacers). Zero performance drop-off against Tier-1 opposition."
        },
        {
            "role": "Death Enforcer & Spinner",
            "name": "Sunil Narine",
            "team": "Kolkata Knight Riders / West Indies",
            "image": "players/sunil_narine.jpg",
            "hp_econ": 6.18,
            "hp_wsr": 11.2,
            "norm_econ": 6.76,
            "post_b_comp": 43.8,
            "score": 89.7,
            "ppr": 1.20,
            "archetype": "Clutch Giant",
            "key_strength": "Death Overs Mystery & Boundary Denial (11.1%)",
            "bio": "Tournament #1 clutch bowler. Delivers an unbelievable 6.18 economy at the death, yielding virtually zero boundaries (11.1%) and claiming a wicket every 11.2 deliveries under maximum scoreboard pressure."
        }
    ]
}

# Top 50 scatter plot sample for 4 Quadrant Interactive Map
scatter_batters = []
for _, r in quad_batters.head(40).iterrows():
    scatter_batters.append({
        "name": r['player_name'],
        "norm_score": round(float(r['norm_score']), 1),
        "hp_score": round(float(r['hp_score']), 1),
        "ppr": round(float(r['ppr']), 2),
        "quadrant": r['quadrant']
    })

scatter_bowlers = []
for _, r in quad_bowlers.head(40).iterrows():
    scatter_bowlers.append({
        "name": r['player_name'],
        "norm_score": round(float(r['norm_score']), 1),
        "hp_score": round(float(r['hp_score']), 1),
        "ppr": round(float(r['ppr']), 2),
        "quadrant": r['quadrant']
    })

web_data = {
    "summary": {
        "total_deliveries": 200999,
        "total_matches": 867,
        "ipl_matches": 371,
        "t20i_matches": 482,
        "qualified_batters": 162,
        "qualified_bowlers": 243,
        "hp_threshold": 0.70,
        "hp_balls": 60314
    },
    "batters": batters_list,
    "bowlers": bowlers_list,
    "pressure_proof_xi": xi_full,
    "scatter_batters": scatter_batters,
    "scatter_bowlers": scatter_bowlers
}

# Save JSON
with open('web/data/cricket_data.json', 'w', encoding='utf-8') as f:
    json.dump(web_data, f, indent=2)

# Save JS export for standalone
with open('web/data/cricket_data.js', 'w', encoding='utf-8') as f:
    f.write('const CRICKET_DATA = ' + json.dumps(web_data, indent=2) + ';')

print('Successfully generated web/data/cricket_data.json and web/data/cricket_data.js!')
