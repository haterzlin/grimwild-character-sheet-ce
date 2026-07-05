#!/usr/bin/env python3
"""Regenerate sheets from the two adventurer shells.

Edit shared layout in adventurer.html and cs/adventurer.html. Edit class-specific
path panels in place. Run this script to sync the repeated shell everywhere.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ORDER = [
    "adventurer",
    "artificer",
    "bard",
    "berseker",
    "cleric",
    "druid",
    "fighter",
    "monk",
    "paladin",
    "psion",
    "ranger",
    "rogue",
    "sorcerer",
    "summoner",
    "swashbuckler",
    "warlock",
    "witch",
    "wizard",
]

EN_NAMES = {
    "adventurer": "Adventurer",
    "artificer": "Artificer",
    "bard": "Bard",
    "berseker": "Berserker",
    "cleric": "Cleric",
    "druid": "Druid",
    "fighter": "Fighter",
    "monk": "Monk",
    "paladin": "Paladin",
    "psion": "Psion",
    "ranger": "Ranger",
    "rogue": "Rogue",
    "sorcerer": "Sorcerer",
    "summoner": "Summoner",
    "swashbuckler": "Swashbuckler",
    "warlock": "Warlock",
    "witch": "Witch",
    "wizard": "Wizard",
}

CS_NAMES = {
    "adventurer": "Dobrodruh",
    "artificer": "Vynálezce",
    "bard": "Bard",
    "berseker": "Berserk",
    "cleric": "Klerik",
    "druid": "Druid",
    "fighter": "Bojovník",
    "monk": "Mnich",
    "paladin": "Paladin",
    "psion": "Psion",
    "ranger": "Hraničář",
    "rogue": "Tulák",
    "sorcerer": "Čaroděj",
    "summoner": "Vyvolávač",
    "swashbuckler": "Šermíř",
    "warlock": "Černokněžník",
    "witch": "Čarodějnice",
    "wizard": "Kouzelník",
}

CS_GENITIVE = {
    "adventurer": "dobrodruha",
    "artificer": "vynálezce",
    "bard": "barda",
    "berseker": "berserka",
    "cleric": "klerika",
    "druid": "druida",
    "fighter": "bojovníka",
    "monk": "mnicha",
    "paladin": "paladina",
    "psion": "psiona",
    "ranger": "hraničáře",
    "rogue": "tuláka",
    "sorcerer": "čaroděje",
    "summoner": "vyvolávače",
    "swashbuckler": "šermíře",
    "warlock": "černokněžníka",
    "witch": "čarodějnice",
    "wizard": "kouzelníka",
}

LANGS = {
    "en": {
        "dir": ROOT,
        "names": EN_NAMES,
        "title": lambda slug: f"Grimwild CE {EN_NAMES[slug]} Sheet",
        "main": lambda slug: f"Grimwild Community Edition {EN_NAMES[slug]} character sheet",
        "nav": "Sheet navigation",
        "prev": "Previous",
        "next": "Next",
    },
    "cs": {
        "dir": ROOT / "cs",
        "names": CS_NAMES,
        "title": lambda slug: f"Grimwild CE Karta {CS_GENITIVE[slug]}",
        "main": lambda slug: f"Karta postavy {CS_GENITIVE[slug]} pro Grimwild Komunitní vydání",
        "nav": "Navigace mezi kartami",
        "prev": "Předchozí",
        "next": "Další",
    },
}

# ponytail: bootstrap-only panels for the P5.2 English additions; edit generated HTML afterward.
NEW_EN_PANELS = {
    "artificer": """      <section class="sheet-panel path-panel">
        <header class="panel-bar">
          <p class="panel-bar-title">Artificer</p>
          <p class="panel-bar-meta">Trackers</p>
        </header>

        <section class="panel-section core-talents">
          <p class="panel-bar-title">Core Talent</p>
          <div class="path-core-layout">
            <div class="path-copy path-copy--core">
              <p><span class="talent-lead control control--pick-filled"></span><strong>Ingenuity:</strong> You harness the power of creativity. You know 6 touchstones from the arcana crucibles, and have created 2 major arcana using them. Anyone can use them with the most relevant stat (as arcana), though it always carries risk for those other than you. Given time, you can: rebuild them using any other touchstones you know - pull off a potent feat of mechanical ingenuity. You can push yourself to do it on the spot.</p>
              <p><strong>Engineer:</strong> Take +1d at creating, repairing, or destroying mechanisms and arcana. You can also deconstruct arcana to learn their touchstones, destroying them in the process.</p>
              <p>[Growth: At levels 2, 4, and 6, gain +1 major arcana and +2 learned touchstones.]</p>
            </div>
          </div>
        </section>

        <section class="panel-section path-talents">
          <p class="panel-bar-title">Path Talents</p>
          <div class="talent-list">
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Animate Objects:</strong> Given time, you can bestow a semblance of life into objects, giving them a 2d Animated power pool. They can only act within their nature or with simple one-word commands. They can roll 1d of their power pool to assist you. You can reliably command up to three of these at a time, with others following their nature.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Animated</span>
                <span class="talent-pool" aria-hidden="true"></span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Artificial Parts:</strong> You have enhanced replacement body parts. Choose 3 benefits for them: built-in weapon - detachable - independent - keen sense - storage - strong. Each perk can be activated once per session to take +1d on a related roll. They also have a drawback: noisy - horrifying - unreliable - power source.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Grenades:</strong> Each session, you have a 3d Grenades resource pool. You have access to the following bombs: entangle - force - fiery - gravity - obscuring - stun. These grenades affect multiple targets or an area.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Grenades</span>
                <span class="talent-pool" aria-hidden="true"></span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Magnum Opus:</strong> You're in the process of creating a mythic arcana. It has a 6d power pool as normal, but before each session, roll 3 random touchstones. Each time, you can choose 1 touchstone to lock in, never rolling for it again.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Mischief Maker:</strong> You can overload arcana to create a potent effect with it. Make a 2d story roll as the magic goes haywire. Add +1t to the story roll each time you use this, clearing them each session.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Mischief</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Trap Making:</strong> Given time, you can set potent traps, with an effect based on the style: blade - collapse - entangle - fire - poison - alarm. Push yourself to deploy a trap on the spot. On a perfect when triggered, take spark.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Push</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Wandslinger:</strong> You have a specialized wand and can use it to fire the following bolts of magic using Wits: acid burst - force blast - ice shard - inferno bolt - static charge - stun beam. Once per session, you can cause a secondary effect (as a critical) related to the type.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
          </div>
        </section>
      </section>""",
    "psion": """      <section class="sheet-panel path-panel path-panel--dense">
        <header class="panel-bar">
          <p class="panel-bar-title">Psion</p>
          <p class="panel-bar-meta">Trackers</p>
        </header>

        <section class="panel-section core-talents">
          <p class="panel-bar-title">Core Talent</p>
          <div class="path-core-layout">
            <div class="path-copy path-copy--core">
              <p><span class="talent-lead control control--pick-filled"></span><strong>Awakened Mind:</strong> You have spellcasting ability. Choose two bastions below which act as the touchstone for your psionic magic. You can cast spells using Wits, and can make them potent by adding instability, eventually adding increasing thorns to your future spellcasting rolls.</p>
              <p>You can't cast potent spells once adding +2t from instability. Thorns from instability can't be ignored and reset at the beginning of each session. You gain more slots that don't add instability with growth.</p>
              <p>[Growth: At levels 3 and 6, gain +1 instability slot at 0d, and +1 bastion.]</p>
            </div>
            <aside class="tracker-panel tracker-panel--top-2_5">
              <div class="tracker-list" aria-hidden="true">
                <div class="tracker-cluster">
                  <p class="tracker-label">+0t</p>
                  <div class="tracker-box-row">
                    <span class="talent-checkbox"></span>
                    <span class="talent-checkbox muted"></span>
                    <span class="talent-checkbox muted"></span>
                  </div>
                </div>
                <div class="tracker-cluster">
                  <p class="tracker-label">+1t</p>
                  <div class="tracker-box-row">
                    <span class="talent-checkbox"></span>
                  </div>
                </div>
                <div class="tracker-cluster">
                  <p class="tracker-label">+2t</p>
                  <div class="tracker-box-row">
                    <span class="talent-checkbox"></span>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <section class="panel-section path-talents">
          <p class="panel-bar-title">Path Talents</p>
          <div class="talent-list">
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Echo:</strong> Once per session, you can create a duplicate as a 3d power pool. It is a second version of you, acting as you with shared knowledge, ability, and resources. You can drop 1d of its pool to have it: assist you - trade places with you.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Foresight:</strong> You can catch small glimpses of the future. Once per session, you can describe a brief course of action while in a calm situation, and the GM will tell you the result. If there's risk, make a montage roll to see how it would play out. Afterward, you can decide whether to take the action.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Mind Blast:</strong> On a critical on a bastion roll, you don't add instability, instead clearing one. This causes mental collateral damage around you: confusion - hallucinations - headaches - panic. One time only, you can make this a ritual-level effect, affecting all within miles.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Psychic Warrior:</strong> You're able to turn your psychic volatility against others. You can create weapons made from pure willpower, using them with Wits. You take +1d to follow up with them when you: take vex - increase your instability level.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Reader:</strong> You gain 1 thread per session and can spend thread when you first meet someone to know their foremost surface thought - they are like an open book to you. If you follow-up on it, it counts as a setup.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Thread</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Tumultuous Mind:</strong> Your fractured mind bleeds into the consciousness of others. The GM judges an NPC's response, or you can spend thread to set it: agitated - confused - paranoid - forgetful. Once per session, when you would take vex, a nearby creature must take it instead.</p>
              </div>
              <div class="talent-slot talent-tag-insp">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Goad Vex</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Shift Form:</strong> Each session, you have a 2d Shifter resource pool. You can roll the pool to alter your features and form, though you keep the same basic shape.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Shift</span>
                <span class="talent-pool" aria-hidden="true"></span>
              </div>
            </article>
          </div>
        </section>
      </section>""",
    "summoner": """      <section class="sheet-panel path-panel path-panel--dense">
        <header class="panel-bar">
          <p class="panel-bar-title">Summoner</p>
          <p class="panel-bar-meta">Trackers</p>
        </header>

        <section class="panel-section core-talents">
          <p class="panel-bar-title">Core Talent</p>
          <div class="path-core-layout">
            <div class="path-copy path-copy--core">
              <p><span class="talent-lead control control--pick-filled"></span><strong>Vassal:</strong> You have a connection with a creature from another plane, and are able to call upon and direct it with a 4d power pool. The pool returns to its max once at 0d, or when you push yourself. It has 1 aspect, a strange trait defining it such as: big enough to ride - flight - swarm - a thematic path talent.</p>
              <p>It can take 1 mark and 1 harm, with any more breaking the anchors holding it here. Make a 2d story roll to see the fallout before it disappears. You can resummon it every scene.</p>
              <p>[Growth: At levels 3 and 6, it gains +1 aspect.]</p>
            </div>
            <aside class="tracker-panel tracker-panel--top-6">
              <div class="tracker-list" aria-hidden="true">
                <div class="tracker-cluster">
                  <p class="tracker-label">Vassal</p>
                  <div class="talent-pool"></div>
                </div>
                <div class="tracker-cluster">
                  <p class="tracker-label">Mark</p>
                  <span class="talent-checkbox"></span>
                </div>
                <div class="tracker-cluster">
                  <p class="tracker-label">Harm</p>
                  <span class="talent-checkbox"></span>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <section class="panel-section path-talents">
          <p class="panel-bar-title">Path Talents</p>
          <div class="talent-list">
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Binding Word:</strong> Add contracts as a wise. If you're present for an agreement, you can make it binding. Both parties know if it's broken, with the defaulting party afflicted by a potent spell, using the contract details as touchstones. One time only, you can make this a ritual-level effect.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Fierce Protector:</strong> Once per session, a creature you control can interrupt an impact move against you. On a grim, they take the impact move instead. Either way, you take +1d on your follow-up against the attacker.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Ley Magic:</strong> Once per session, you can temporarily alter the leylines in the area to: draw or repel certain creatures - enhance or dampen magic. When you alter a place like this, you know when others enter the area. You can push yourself to do it again.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Monster Menagerie:</strong> You have a bond with 3 different creatures, all with their own aspects. When you summon a vassal, you can choose which answers the call.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Pocket Plane:</strong> Given time, you can open a hole to a small pocket dimension about the size of a room. You can push yourself to open it on the spot. If dropped, make a story roll to see what happens inside as the plane collapses. You don't need anchors for planar travel rituals.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Push</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Portal Network:</strong> Given time, you can: establish a waypoint in your network - open a portal from one waypoint to another. You can push yourself to make a temporary link in the moment, but doing so carries risk. Those around you can use the portal as well. Define how you travel, such as by: shadows - trees - doorways - dreams.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Push</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Shared Soul:</strong> You can merge with your vassal, sharing path talents, aspects, and incoming harm. You can choose to use the power pool or your own stats, and when your anchors break, take +1d on the story roll.</p>
              </div>
            </article>
          </div>
        </section>
      </section>""",
    "swashbuckler": """      <section class="sheet-panel path-panel">
        <header class="panel-bar">
          <p class="panel-bar-title">Swashbuckler</p>
          <p class="panel-bar-meta">Trackers</p>
        </header>

        <section class="panel-section core-talents">
          <p class="panel-bar-title">Core Talent</p>
          <div class="path-core-layout">
            <div class="path-copy path-copy--core">
              <p><span class="talent-lead control control--pick-filled"></span><strong>Panache:</strong> You wield the spotlight as well as any blade, allowing great feats of charm and skill. Each scene, you have 2 panache to fuel your derring-do. Before making a roll, you can spend panache, removing that many thorns. If you remove all thorns, they become panache dice instead, increasing the final result level on a 7 or 8. When one of your rolls is cut by a thorn, you gain 1 panache (ignoring your max).</p>
              <p><strong>Quick Wit:</strong> Once per session, you can interrupt an impact move with a: humorous quip - quick flourish - timely distraction.</p>
              <p>[Growth: At levels 2, 4, and 6, gain +1 panache per scene.]</p>
            </div>
            <aside class="tracker-panel tracker-panel--top-6">
              <div class="tracker-list" aria-hidden="true">
                <div class="tracker-cluster">
                  <p class="tracker-label">Panache</p>
                  <div class="tracker-box-row">
                    <span class="talent-checkbox"></span>
                    <span class="talent-checkbox"></span>
                    <span class="talent-checkbox muted"></span>
                  </div>
                  <div class="tracker-box-row">
                    <span class="talent-checkbox muted"></span>
                    <span class="talent-checkbox muted"></span>
                  </div>
                </div>
                <div class="tracker-cluster">
                  <p class="tracker-label">Interrupt</p>
                  <span class="talent-checkbox"></span>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <section class="panel-section path-talents">
          <p class="panel-bar-title">Path Talents</p>
          <div class="talent-list">
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Audacity:</strong> When you act with pure reckless abandon, 5s count as 6s, but 4s count as 1s on a follow-up. Regardless of the outcome, those around you are briefly struck by: awe - bewilderment - panic - excitement.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Fancy Footwork:</strong> On a perfect when you fight to setup an advantage or otherwise improve your positioning, you can roll a related task pool by: seizing an opening - unnerving your foe.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Improvise:</strong> Once per session, you can describe your creative use of your surroundings to take +1d. These improvised weapons and tools often stretch the bounds of reality with their use. You can push yourself to do it again.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Use</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Lucky:</strong> Each session you have a 1d Luck pool. You can roll it as a bonus die after any roll you make and story rolls related to you. On a grim, take spark.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Luck</span>
                <span class="talent-pool" aria-hidden="true"></span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Natural Moxie:</strong> Choose two skills from the Expertise talent (pg. 67). Take +1d when using these skills. [Prohibited: Rogue]</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Provoke:</strong> Once per session, through insult, boast, or challenge, you can goad the GM into spending suspense on an impact move targeting only you. You take +1d on the defense roll, and on a perfect, they: are compelled to keep lashing out - leave an opening - are utterly embarrassed.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Goad</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>The Legend Of...:</strong> Many recognize you as a hero, others as a cad and ne'er-do-well. Track tales of your exploits with campaign pools. When you play into it by: leaving a calling card - saying your catchphrase in a dramatic moment - indulging a fan, take spark.</p>
              </div>
            </article>
          </div>
        </section>
      </section>""",
    "witch": """      <section class="sheet-panel path-panel">
        <header class="panel-bar">
          <p class="panel-bar-title">Witch</p>
          <p class="panel-bar-meta">Trackers</p>
        </header>

        <section class="panel-section core-talents">
          <p class="panel-bar-title">Core Talent</p>
          <div class="path-core-layout">
            <div class="path-copy path-copy--core">
              <p><span class="talent-lead control control--pick-filled"></span><strong>Words of Power:</strong> You understand the ancient magic inherent in the world. You have spellcasting ability, rolling Presence to cast using any 2 words of power as the touchstones. When you use a word, burn it - you can't use it again until the next session. Given time, you can make this spell potent. You begin with 6 words of power from the crucible. Spells without risk are automatically successful and don't burn words, unless potent.</p>
              <p><strong>Ritualist:</strong> Take +1d when completing ritual invocations, and you can use relevant words of power as anchors.</p>
              <p>[Growth: At levels 2, 4, and 6, gain +2 words of power.]</p>
            </div>
          </div>
        </section>

        <section class="panel-section path-talents">
          <p class="panel-bar-title">Path Talents</p>
          <div class="talent-list">
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Bailiwick:</strong> You are known to other witches by a title and the power inherent in your magical domain - your Bailiwick. Choose 1 word of power. You can burn any other word to use it, and on a critical, you regain the use of all words.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Evil Eye:</strong> You can roll Presence to hex someone with: dread - clumsiness - confusion - forgetfulness - misfortune - sleepiness. Decide when it takes effect: now - soon - much later - specific trigger. This magic only works on someone once.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Familiar:</strong> You manifest a small magical creature. You can communicate telepathically, use its senses, and send it on simple tasks, making a story roll to see how it goes. You can also push yourself to cast a spell through it. If your familiar takes damage, it vanishes and reappears at the start of the next scene.</p>
              </div>
              <div class="talent-slot">
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span>Push</span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Herbalism:</strong> Before each session, use the herbalism crucible (pg. 83) to make two herb names. Each session, you have 1 trivial and 1 minor potion, chosen when they're used. The name is the touchstone. One time only, you can have 1 major potion.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Minor</span>
                <span class="talent-checkbox" aria-hidden="true"></span>
                <span class="talent-tag-label">Major</span>
                <span class="talent-checkbox" aria-hidden="true"></span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Homely Hovel:</strong> Given time, you can bless a homestead to overflow with power. You get outside help on all rolls while on its grounds. Choose two wondrous traits to give it such as: traveling - ritual anchor - healing - caretaker. You can only have one homestead like this at a time.</p>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Soothsayer:</strong> Once per session, you can tag a spirit in the local area. They offer a 3d Spirit pool rolled as bonus dice when you or an ally invokes their domain. They may ask for aid in return. Spirit domains include things such as: rivers - the night sky - art - furry critters.</p>
              </div>
              <div class="talent-slot talent-slot--stack-center">
                <span class="talent-tag-label">Spirits</span>
                <span class="talent-pool" aria-hidden="true"></span>
              </div>
            </article>
            <article class="talent-row">
              <div class="talent-picker control control--pick" aria-hidden="true"></div>
              <div class="path-copy talent-body">
                <p><strong>Wonder Magnet:</strong> You can cause wild surges when spellcasting, as the magical twist in Sorcery. When it triggers, make a 3d story roll for the results. On a perfect, take spark. When strange things happen, they happen to you.</p>
              </div>
            </article>
          </div>
        </section>
      </section>""",
}

CS_BASE_REPLACEMENTS = [
    ("Trackers", "Ukazatele"),
    ("Core Talent", "Hlavní talent"),
    ("Path Talents", "Talenty cesty"),
    ("Use", "Použití"),
    ("Push", "Překonat"),
]

CS_PANEL_REPLACEMENTS = {
    "artificer": [
        ("Artificer", "Vynálezce"),
        ("""<strong>Ingenuity:</strong> You harness the power of creativity. You know 6 touchstones from the arcana crucibles, and have created 2 major arcana using them. Anyone can use them with the most relevant stat (as arcana), though it always carries risk for those other than you. Given time, you can: rebuild them using any other touchstones you know - pull off a potent feat of mechanical ingenuity. You can push yourself to do it on the spot.""", """<strong>Vynalézavost:</strong> Spoutáváš moc tvořivosti. Znáš 6 ohnisek z tyglíků arkan a vytvořil jsi pomocí nich 2 silná arkana. Kdokoli je může použít s nejvhodnější vlastností jako arkana, pro každého kromě tebe však vždy nesou riziko. Když máš čas, můžeš je přestavět s jinými známými ohnisky nebo provést mocný čin mechanické vynalézavosti. Můžeš se překonat a zvládnout to okamžitě."""),
        ("""<strong>Engineer:</strong> Take +1d at creating, repairing, or destroying mechanisms and arcana. You can also deconstruct arcana to learn their touchstones, destroying them in the process.""", """<strong>Inženýr:</strong> Máš +1 kostku při vytváření, opravách nebo ničení mechanismů a arkan. Arkana můžeš také rozebrat a naučit se jejich ohniska; tím je zničíš."""),
        ("[Growth: At levels 2, 4, and 6, gain +1 major arcana and +2 learned touchstones.]", "[Růst: Na úrovních 2, 4 a 6 získej +1 silnou arkanu a +2 naučená ohniska.]"),
        ("""<strong>Animate Objects:</strong> Given time, you can bestow a semblance of life into objects, giving them a 2d Animated power pool. They can only act within their nature or with simple one-word commands. They can roll 1d of their power pool to assist you. You can reliably command up to three of these at a time, with others following their nature.""", """<strong>Oživování předmětů:</strong> Když máš čas, můžeš předmětům propůjčit náznak života a dát jim bank 2 kostek oživení. Jednají jen podle své povahy nebo podle jednoduchých jednoslovných příkazů. Mohou hodit 1 kostkou ze svého banku, aby ti pomohly. Spolehlivě ovládáš až tři najednou; ostatní následují svou povahu."""),
        ("""<strong>Artificial Parts:</strong> You have enhanced replacement body parts. Choose 3 benefits for them: built-in weapon - detachable - independent - keen sense - storage - strong. Each perk can be activated once per session to take +1d on a related roll. They also have a drawback: noisy - horrifying - unreliable - power source.""", """<strong>Umělé části:</strong> Máš vylepšené náhradní části těla. Vyber 3 výhody: vestavěná zbraň - odnímatelné - samostatné - ostrý smysl - úložný prostor - silné. Každou výhodu můžeš jednou za sezení aktivovat pro +1 kostku k souvisejícímu hodu. Mají také nevýhodu: hlučné - děsivé - nespolehlivé - zdroj energie."""),
        ("""<strong>Grenades:</strong> Each session, you have a 3d Grenades resource pool. You have access to the following bombs: entangle - force - fiery - gravity - obscuring - stun. These grenades affect multiple targets or an area.""", """<strong>Granáty:</strong> Každé sezení máš bank 3 kostek granátů. Máš přístup k bombám: poutací - silová - ohnivá - gravitační - zahalující - omračující. Granáty zasahují více cílů nebo oblast."""),
        ("""<strong>Magnum Opus:</strong> You're in the process of creating a mythic arcana. It has a 6d power pool as normal, but before each session, roll 3 random touchstones. Each time, you can choose 1 touchstone to lock in, never rolling for it again.""", """<strong>Magnum opus:</strong> Pracuješ na vytvoření mýtického arkana. Má běžný bank 6 kostek moci, ale před každým sezením hoď 3 náhodná ohniska. Pokaždé můžeš 1 ohnisko uzamknout a už ho nikdy neházet znovu."""),
        ("""<strong>Mischief Maker:</strong> You can overload arcana to create a potent effect with it. Make a 2d story roll as the magic goes haywire. Add +1t to the story roll each time you use this, clearing them each session.""", """<strong>Potížista:</strong> Můžeš přetížit arkana a vyvolat s nimi mocný účinek. Hoď na příběh 2 kostkami, když se magie utrhne ze řetězu. Pokaždé, když to použiješ, přidej k hodu +1 trn; trny se mažou každé sezení."""),
        ("""<strong>Trap Making:</strong> Given time, you can set potent traps, with an effect based on the style: blade - collapse - entangle - fire - poison - alarm. Push yourself to deploy a trap on the spot. On a perfect when triggered, take spark.""", """<strong>Výroba pastí:</strong> Když máš čas, můžeš nastražit mocné pasti s účinkem podle stylu: čepel - zával - poutání - oheň - jed - poplach. Překonej se a polož past okamžitě. Při dokonalém výsledku při spuštění získej jiskru."""),
        ("""<strong>Wandslinger:</strong> You have a specialized wand and can use it to fire the following bolts of magic using Wits: acid burst - force blast - ice shard - inferno bolt - static charge - stun beam. Once per session, you can cause a secondary effect (as a critical) related to the type.""", """<strong>Mistr hůlky:</strong> Máš specializovanou hůlku a Důvtipem z ní střílíš magické střely: kyselinový výboj - silový výbuch - ledový střep - pekelný blesk - statický náboj - omračující paprsek. Jednou za sezení můžeš způsobit vedlejší účinek podle typu, jako při kritickém úspěchu."""),
        ("Animated", "Oživení"),
        ("Grenades", "Granáty"),
        ("Mischief", "Neplecha"),
    ],
    "psion": [
        ("""<strong>Awakened Mind:</strong> You have spellcasting ability. Choose two bastions below which act as the touchstone for your psionic magic. You can cast spells using Wits, and can make them potent by adding instability, eventually adding increasing thorns to your future spellcasting rolls.""", """<strong>Probuzená mysl:</strong> Umíš kouzlit. Vyber dva bastiony níže; slouží jako ohniska tvé psionické magie. Kouzlíš hodem Důvtipem a můžeš kouzla učinit mocnými přidáním nestability, která postupně přidává rostoucí trny k budoucím hodům na kouzlení."""),
        ("""You can't cast potent spells once adding +2t from instability. Thorns from instability can't be ignored and reset at the beginning of each session. You gain more slots that don't add instability with growth.""", """Nemůžeš sesílat mocná kouzla, jakmile z nestability přidáváš +2 trny. Trny z nestability nelze ignorovat a obnovují se na začátku každého sezení. S růstem získáš další políčka bez přidání nestability."""),
        ("[Growth: At levels 3 and 6, gain +1 instability slot at 0d, and +1 bastion.]", "[Růst: Na úrovních 3 a 6 získej +1 políčko nestability na +0 trnů a +1 baštu.]"),
        ("""<strong>Echo:</strong> Once per session, you can create a duplicate as a 3d power pool. It is a second version of you, acting as you with shared knowledge, ability, and resources. You can drop 1d of its pool to have it: assist you - trade places with you.""", """<strong>Ozvěna:</strong> Jednou za sezení můžeš vytvořit dvojníka jako bank 3 kostek moci. Je to druhá verze tebe, jedná jako ty a sdílí tvé znalosti, schopnosti i zdroje. Můžeš odebrat 1 kostku z jeho banku, aby ti pomohl nebo si s tebou vyměnil místo."""),
        ("""<strong>Foresight:</strong> You can catch small glimpses of the future. Once per session, you can describe a brief course of action while in a calm situation, and the GM will tell you the result. If there's risk, make a montage roll to see how it would play out. Afterward, you can decide whether to take the action.""", """<strong>Předtucha:</strong> Zahlédáš drobné záblesky budoucnosti. Jednou za sezení můžeš v klidné situaci popsat krátký postup a vypravěč ti řekne výsledek. Pokud hrozí riziko, hoď montážní hod, jak by to dopadlo. Poté se rozhodni, zda akci provedeš."""),
        ("""<strong>Mind Blast:</strong> On a critical on a bastion roll, you don't add instability, instead clearing one. This causes mental collateral damage around you: confusion - hallucinations - headaches - panic. One time only, you can make this a ritual-level effect, affecting all within miles.""", """<strong>Mentální výbuch:</strong> Při kritickém úspěchu v hodu baštou nepřidáš nestabilitu, místo toho jednu smažeš. Kolem tebe to způsobí duševní vedlejší škody: zmatek - halucinace - bolesti hlavy - paniku. Jen jednou z toho můžeš udělat účinek na úrovni rituálu, zasahující míle daleko."""),
        ("""<strong>Psychic Warrior:</strong> You're able to turn your psychic volatility against others. You can create weapons made from pure willpower, using them with Wits. You take +1d to follow up with them when you: take vex - increase your instability level.""", """<strong>Psychický válečník:</strong> Obracíš svou psychickou nestálost proti ostatním. Dokážeš tvořit zbraně z čisté vůle a používat je Důvtipem. Máš +1 kostku na navazující akci s nimi, když utrpíš rozrušení nebo zvýšíš úroveň nestability."""),
        ("""<strong>Reader:</strong> You gain 1 thread per session and can spend thread when you first meet someone to know their foremost surface thought - they are like an open book to you. If you follow-up on it, it counts as a setup.""", """<strong>Čtenář:</strong> Získáš 1 zápletku za sezení. Když někoho poprvé potkáš, můžeš vnést zápletku a znát jeho nejsilnější povrchovou myšlenku; je pro tebe jako otevřená kniha. Pokud na ni navážeš, počítá se jako příprava."""),
        ("""<strong>Tumultuous Mind:</strong> Your fractured mind bleeds into the consciousness of others. The GM judges an NPC's response, or you can spend thread to set it: agitated - confused - paranoid - forgetful. Once per session, when you would take vex, a nearby creature must take it instead.""", """<strong>Bouřlivá mysl:</strong> Tvá roztříštěná mysl prosakuje do vědomí ostatních. Reakci NPC posoudí vypravěč, nebo vnes zápletku a nastav ji: rozrušená - zmatená - paranoidní - zapomnětlivá. Jednou za sezení, když bys utrpěl rozrušení, ho místo tebe utrpí blízký tvor."""),
        ("""<strong>Shift Form:</strong> Each session, you have a 2d Shifter resource pool. You can roll the pool to alter your features and form, though you keep the same basic shape.""", """<strong>Proměna podoby:</strong> Každé sezení máš bank 2 kostek proměny. Můžeš ho hodit a změnit své rysy a podobu, ale zachováš si stejný základní tvar."""),
        ("Psion", "Psion"),
        ("Thread", "Zápletka"),
        ("Goad Vex", "Vyvolej rozr."),
        ("Shift", "Proměna"),
    ],
    "summoner": [
        ("Summoner", "Vyvolávač"),
        ("""<strong>Vassal:</strong> You have a connection with a creature from another plane, and are able to call upon and direct it with a 4d power pool. The pool returns to its max once at 0d, or when you push yourself. It has 1 aspect, a strange trait defining it such as: big enough to ride - flight - swarm - a thematic path talent.""", """<strong>Vazal:</strong> Máš spojení s bytostí z jiné sféry a dokážeš ji přivolat a řídit bankem 4 kostek moci. Bank se jednou obnoví na maximum při 0 kostkách nebo když se překonáš. Má 1 aspekt, zvláštní rys, který ji definuje, třeba: dost velká k jízdě - let - roj - tematický talent cesty."""),
        ("""It can take 1 mark and 1 harm, with any more breaking the anchors holding it here. Make a 2d story roll to see the fallout before it disappears. You can resummon it every scene.""", """Může utrpět 1 značku a 1 újmu; cokoli dalšího zlomí kotvy, které ji zde drží. Hoď na příběh 2 kostkami, jaké následky nastanou, než zmizí. Každou scénu ji můžeš znovu vyvolat."""),
        ("[Growth: At levels 3 and 6, it gains +1 aspect.]", "[Růst: Na úrovních 3 a 6 získá +1 aspekt.]"),
        ("""<strong>Binding Word:</strong> Add contracts as a wise. If you're present for an agreement, you can make it binding. Both parties know if it's broken, with the defaulting party afflicted by a potent spell, using the contract details as touchstones. One time only, you can make this a ritual-level effect.""", """<strong>Svazující slovo:</strong> Přidej smlouvy jako znalost. Jsi-li přítomen dohodě, můžeš ji učinit závaznou. Obě strany poznají, když je porušena; stranu, která selže, zasáhne mocné kouzlo s detaily smlouvy jako ohnisky. Jen jednou z toho můžeš udělat účinek na úrovni rituálu."""),
        ("""<strong>Fierce Protector:</strong> Once per session, a creature you control can interrupt an impact move against you. On a grim, they take the impact move instead. Either way, you take +1d on your follow-up against the attacker.""", """<strong>Divoký ochránce:</strong> Jednou za sezení může tvor, kterého ovládáš, přerušit určení následků proti tobě. Při chmurném výsledku ho utrpí místo tebe. V každém případě máš +1 kostku na navazující akci proti útočníkovi."""),
        ("""<strong>Ley Magic:</strong> Once per session, you can temporarily alter the leylines in the area to: draw or repel certain creatures - enhance or dampen magic. When you alter a place like this, you know when others enter the area. You can push yourself to do it again.""", """<strong>Magie ley linií:</strong> Jednou za sezení můžeš dočasně změnit ley linie v oblasti, aby přitahovaly nebo odpuzovaly určité tvory, případně posílily nebo tlumily magii. Když tak místo změníš, víš, kdy do oblasti vstoupí ostatní. Můžeš se překonat a udělat to znovu."""),
        ("""<strong>Monster Menagerie:</strong> You have a bond with 3 different creatures, all with their own aspects. When you summon a vassal, you can choose which answers the call.""", """<strong>Bestiář:</strong> Máš pouto se 3 různými tvory, každý má své vlastní aspekty. Když vyvoláváš vazala, vyber, který odpoví na volání."""),
        ("""<strong>Pocket Plane:</strong> Given time, you can open a hole to a small pocket dimension about the size of a room. You can push yourself to open it on the spot. If dropped, make a story roll to see what happens inside as the plane collapses. You don't need anchors for planar travel rituals.""", """<strong>Kapesní sféra:</strong> Když máš čas, můžeš otevřít průchod do malé kapesní dimenze velké asi jako místnost. Můžeš se překonat a otevřít ji okamžitě. Pokud je zrušena, hoď na příběh, co se uvnitř stane při zhroucení sféry. Pro rituály cestování sférami nepotřebuješ kotvy."""),
        ("""<strong>Portal Network:</strong> Given time, you can: establish a waypoint in your network - open a portal from one waypoint to another. You can push yourself to make a temporary link in the moment, but doing so carries risk. Those around you can use the portal as well. Define how you travel, such as by: shadows - trees - doorways - dreams.""", """<strong>Síť portálů:</strong> Když máš čas, můžeš založit bod ve své síti nebo otevřít portál z jednoho bodu do druhého. Můžeš se překonat a vytvořit dočasné spojení okamžitě, ale nese to riziko. Portál mohou použít i lidé kolem tebe. Urči, jak cestuješ: stíny - stromy - dveřmi - sny."""),
        ("""<strong>Shared Soul:</strong> You can merge with your vassal, sharing path talents, aspects, and incoming harm. You can choose to use the power pool or your own stats, and when your anchors break, take +1d on the story roll.""", """<strong>Sdílená duše:</strong> Můžeš splynout se svým vazalem a sdílet talenty cesty, aspekty i příchozí újmu. Můžeš použít bank moci nebo vlastní vlastnosti, a když se tvé kotvy zlomí, máš +1 kostku k hodu na příběh."""),
        ("Vassal", "Vazal"),
        ("Mark", "Značka"),
        ("Harm", "Újma"),
    ],
    "swashbuckler": [
        ("Swashbuckler", "Šermíř"),
        ("""<strong>Panache:</strong> You wield the spotlight as well as any blade, allowing great feats of charm and skill. Each scene, you have 2 panache to fuel your derring-do. Before making a roll, you can spend panache, removing that many thorns. If you remove all thorns, they become panache dice instead, increasing the final result level on a 7 or 8. When one of your rolls is cut by a thorn, you gain 1 panache (ignoring your max).""", """<strong>Švih:</strong> Vládneš záběrem stejně obratně jako čepelí a dokážeš velké činy šarmu a dovednosti. Každou scénu máš 2 švihu na odvážné kousky. Před hodem můžeš utratit švih a odebrat tolik trnů. Pokud odebereš všechny trny, stanou se místo toho kostkami švihu, které při 7 nebo 8 zvýší konečnou úroveň výsledku. Když je některý tvůj hod seříznut trnem, získej 1 švih, i nad maximum."""),
        ("""<strong>Quick Wit:</strong> Once per session, you can interrupt an impact move with a: humorous quip - quick flourish - timely distraction.""", """<strong>Pohotový vtip:</strong> Jednou za sezení můžeš přerušit určení následků pomocí: vtipné poznámky - rychlé parády - včasného rozptýlení."""),
        ("[Growth: At levels 2, 4, and 6, gain +1 panache per scene.]", "[Růst: Na úrovních 2, 4 a 6 získej +1 švih za scénu.]"),
        ("""<strong>Audacity:</strong> When you act with pure reckless abandon, 5s count as 6s, but 4s count as 1s on a follow-up. Regardless of the outcome, those around you are briefly struck by: awe - bewilderment - panic - excitement.""", """<strong>Drzost:</strong> Když jednáš s čistou bezhlavou odvahou, 5 se počítají jako 6, ale 4 jako 1 na navazující akci. Bez ohledu na výsledek jsou lidé kolem krátce zasaženi: úžasem - omámením - panikou - vzrušením."""),
        ("""<strong>Fancy Footwork:</strong> On a perfect when you fight to setup an advantage or otherwise improve your positioning, you can roll a related task pool by: seizing an opening - unnerving your foe.""", """<strong>Elegantní kroky:</strong> Při dokonalém výsledku, když bojuješ pro přípravu výhody nebo jinak zlepšuješ pozici, můžeš hodit související bank úkolu tím, že využiješ skulinu nebo znejistíš protivníka."""),
        ("""<strong>Improvise:</strong> Once per session, you can describe your creative use of your surroundings to take +1d. These improvised weapons and tools often stretch the bounds of reality with their use. You can push yourself to do it again.""", """<strong>Improvizace:</strong> Jednou za sezení můžeš popsat tvořivé využití okolí a získat +1 kostku. Tyto improvizované zbraně a nástroje často napínají hranice reality. Můžeš se překonat a udělat to znovu."""),
        ("""<strong>Lucky:</strong> Each session you have a 1d Luck pool. You can roll it as a bonus die after any roll you make and story rolls related to you. On a grim, take spark.""", """<strong>Štístko:</strong> Každé sezení máš bank s 1 kostkou štěstí. Můžeš ho hodit jako bonusovou kostku po libovolném svém hodu a po hodech na příběh, které se tě týkají. Při chmurném výsledku získej jiskru."""),
        ("""<strong>Natural Moxie:</strong> Choose two skills from the Expertise talent (pg. 67). Take +1d when using these skills. [Prohibited: Rogue]""", """<strong>Přirozená kuráž:</strong> Vyber dvě dovednosti z talentu Odbornost (str. 67). Při jejich použití máš +1 kostku. [Zakázáno: Tulák]"""),
        ("""<strong>Provoke:</strong> Once per session, through insult, boast, or challenge, you can goad the GM into spending suspense on an impact move targeting only you. You take +1d on the defense roll, and on a perfect, they: are compelled to keep lashing out - leave an opening - are utterly embarrassed.""", """<strong>Provokace:</strong> Jednou za sezení můžeš urážkou, chlubením nebo výzvou přimět vypravěče utratit napětí za určení následků mířené jen na tebe. Na obranný hod máš +1 kostku a při dokonalém výsledku protivník dál útočí, nechá odkrytí nebo se zcela znemožní."""),
        ("""<strong>The Legend Of...:</strong> Many recognize you as a hero, others as a cad and ne'er-do-well. Track tales of your exploits with campaign pools. When you play into it by: leaving a calling card - saying your catchphrase in a dramatic moment - indulging a fan, take spark.""", """<strong>Legenda o...:</strong> Mnozí tě znají jako hrdinu, jiní jako darebáka a budižkničemu. Pověsti o svých činech sleduj kampaňovými pooly. Když jim jdeš naproti tím, že necháš vizitku, proneseš hlášku v dramatické chvíli nebo se věnuješ fanouškovi, získej jiskru."""),
        ("Panache", "Švih"),
        ("Interrupt", "Přerušení"),
        ("Luck", "Štěstí"),
        ("Goad", "Vyvolej"),
    ],
    "witch": [
        ("Witch", "Čarodějnice"),
        ("""<strong>Words of Power:</strong> You understand the ancient magic inherent in the world. You have spellcasting ability, rolling Presence to cast using any 2 words of power as the touchstones. When you use a word, burn it - you can't use it again until the next session. Given time, you can make this spell potent. You begin with 6 words of power from the crucible. Spells without risk are automatically successful and don't burn words, unless potent.""", """<strong>Slova moci:</strong> Rozumíš prastaré magii přítomné ve světě. Umíš kouzlit hodem Charismem a jako ohniska používáš libovolná 2 slova moci. Když slovo použiješ, spálíš ho; nemůžeš ho použít znovu do dalšího sezení. Když máš čas, můžeš kouzlo učinit mocným. Začínáš se 6 slovy moci z tyglíku. Kouzla bez rizika automaticky uspějí a nespalují slova, pokud nejsou mocná."""),
        ("""<strong>Ritualist:</strong> Take +1d when completing ritual invocations, and you can use relevant words of power as anchors.""", """<strong>Ritualista:</strong> Máš +1 kostku při dokončování vzývání rituálů a můžeš používat relevantní slova moci jako kotvy."""),
        ("[Growth: At levels 2, 4, and 6, gain +2 words of power.]", "[Růst: Na úrovních 2, 4 a 6 získej +2 slova moci.]"),
        ("""<strong>Bailiwick:</strong> You are known to other witches by a title and the power inherent in your magical domain - your Bailiwick. Choose 1 word of power. You can burn any other word to use it, and on a critical, you regain the use of all words.""", """<strong>Hájemství:</strong> Ostatní čarodějnice tě znají podle titulu a moci tvé magické domény - tvého hájemství. Vyber 1 slovo moci. Můžeš spálit libovolné jiné slovo, abys ho použila, a při kritickém úspěchu obnovíš použití všech slov."""),
        ("""<strong>Evil Eye:</strong> You can roll Presence to hex someone with: dread - clumsiness - confusion - forgetfulness - misfortune - sleepiness. Decide when it takes effect: now - soon - much later - specific trigger. This magic only works on someone once.""", """<strong>Zlé oko:</strong> Hoď Charismem, když někoho uhraneš: děsem - nemotorností - zmatkem - zapomnětlivostí - smůlou - ospalostí. Urči, kdy se projeví: teď - brzy - mnohem později - konkrétním spouštěčem. Tato magie na někoho funguje jen jednou."""),
        ("""<strong>Familiar:</strong> You manifest a small magical creature. You can communicate telepathically, use its senses, and send it on simple tasks, making a story roll to see how it goes. You can also push yourself to cast a spell through it. If your familiar takes damage, it vanishes and reappears at the start of the next scene.""", """<strong>Familiar:</strong> Projevíš malou magickou bytost. Komunikujete telepaticky, používáš její smysly a posíláš ji na jednoduché úkoly; hoď na příběh, jak to dopadne. Můžeš se také překonat a seslat kouzlo skrze ni. Pokud utrpí zranění, zmizí a objeví se na začátku další scény."""),
        ("""<strong>Herbalism:</strong> Before each session, use the herbalism crucible (pg. 83) to make two herb names. Each session, you have 1 trivial and 1 minor potion, chosen when they're used. The name is the touchstone. One time only, you can have 1 major potion.""", """<strong>Bylinkářství:</strong> Před každým sezením použij bylinkářský tyglík (str. 83) a vytvoř dvě jména bylin. Každé sezení máš 1 triviální a 1 slabší lektvar, vybrané při použití. Jméno je ohnisko. Jen jednou můžeš mít 1 silný lektvar."""),
        ("""<strong>Homely Hovel:</strong> Given time, you can bless a homestead to overflow with power. You get outside help on all rolls while on its grounds. Choose two wondrous traits to give it such as: traveling - ritual anchor - healing - caretaker. You can only have one homestead like this at a time.""", """<strong>Útulná chýše:</strong> Když máš čas, můžeš požehnat domovu, aby překypoval mocí. Na jeho pozemku máš vnější pomoc ke všem hodům. Dej mu dva podivuhodné rysy, třeba: putující - rituální kotva - léčivý - opatrovník. Najednou můžeš mít jen jeden takový domov."""),
        ("""<strong>Soothsayer:</strong> Once per session, you can tag a spirit in the local area. They offer a 3d Spirit pool rolled as bonus dice when you or an ally invokes their domain. They may ask for aid in return. Spirit domains include things such as: rivers - the night sky - art - furry critters.""", """<strong>Věštkyně:</strong> Jednou za sezení můžeš označit ducha v okolí. Nabídne bank 3 kostek ducha, který se hází jako bonusové kostky, když ty nebo spojenec vzýváte jeho doménu. Na oplátku může žádat pomoc. Domény duchů mohou být: řeky - noční obloha - umění - chlupatá zvířátka."""),
        ("""<strong>Wonder Magnet:</strong> You can cause wild surges when spellcasting, as the magical twist in Sorcery. When it triggers, make a 3d story roll for the results. On a perfect, take spark. When strange things happen, they happen to you.""", """<strong>Magnet na zázraky:</strong> Při kouzlení můžeš způsobovat divoké přívaly jako magický zvrat u Čarodějnictví. Když se spustí, hoď na příběh 3 kostkami pro výsledek. Při dokonalém výsledku získej jiskru. Když se dějí divné věci, dějí se ti."""),
        ("Minor", "Slabší"),
        ("Major", "Silný"),
        ("Spirits", "Duchové"),
    ],
}


def translated_panel(slug: str) -> str:
    panel = NEW_EN_PANELS[slug]
    if "path-panel--dense" not in panel:
        panel = panel.replace("sheet-panel path-panel", "sheet-panel path-panel path-panel--dense", 1)
    for old, new in CS_PANEL_REPLACEMENTS[slug] + CS_BASE_REPLACEMENTS:
        panel = panel.replace(old, new)
    return panel


NEW_CS_PANELS = {slug: translated_panel(slug) for slug in NEW_EN_PANELS}

PATH_PANEL_START = '      <section class="sheet-panel path-panel'
PATH_PANEL_END = '\n\n      <section class="sheet-panel traits-panel">'
NAV_RE = re.compile(r'  <nav class="sheet-nav" aria-label="[^"]+">\n.*?\n  </nav>', re.S)


def sheet_path(lang: str, slug: str) -> Path:
    return LANGS[lang]["dir"] / f"{slug}.html"


def slugs_for_lang(lang: str) -> list[str]:
    root = LANGS[lang]["dir"]
    names = LANGS[lang]["names"]
    new_panels = {"en": NEW_EN_PANELS, "cs": NEW_CS_PANELS}[lang]
    return [
        slug
        for slug in ORDER
        if slug in names and (sheet_path(lang, slug).exists() or slug in new_panels)
    ]


def path_panel(html: str) -> str:
    start = html.index(PATH_PANEL_START)
    end = html.index(PATH_PANEL_END, start)
    return html[start:end]


def replace_path_panel(html: str, panel: str) -> str:
    start = html.index(PATH_PANEL_START)
    end = html.index(PATH_PANEL_END, start)
    # ponytail: generated HTML is the source for path panels; split fragments if that gets annoying.
    return html[:start] + panel + html[end:]


def nav(lang: str, slug: str) -> str:
    meta = LANGS[lang]
    slugs = slugs_for_lang(lang)
    index = slugs.index(slug)
    prev_slug = slugs[index - 1]
    next_slug = slugs[(index + 1) % len(slugs)]
    return f"""  <nav class="sheet-nav" aria-label="{meta["nav"]}">
    <a class="sheet-nav-link" href="{prev_slug}.html" rel="prev">&larr; {meta["prev"]}: {meta["names"][prev_slug]}</a>
    <a class="sheet-nav-link sheet-nav-link--next" href="{next_slug}.html" rel="next">{meta["next"]}: {meta["names"][next_slug]} &rarr;</a>
  </nav>"""


def render(lang: str, slug: str, template: str, panel: str) -> str:
    meta = LANGS[lang]
    html = re.sub(r"  <title>.*</title>", f"  <title>{meta['title'](slug)}</title>", template, count=1)
    html = re.sub(
        r'  <main class="sheet-workspace" aria-label="[^"]+">',
        f'  <main class="sheet-workspace" aria-label="{meta["main"](slug)}">',
        html,
        count=1,
    )
    html = replace_path_panel(html, panel)
    html = NAV_RE.sub(nav(lang, slug), html, count=1)
    return html


def regenerate(check: bool, langs: list[str]) -> list[Path]:
    changed = []
    for lang in langs:
        template = sheet_path(lang, "adventurer").read_text(encoding="utf-8")
        for slug in slugs_for_lang(lang):
            path = sheet_path(lang, slug)
            if path.exists():
                old = path.read_text(encoding="utf-8")
                panel = path_panel(old)
            else:
                old = ""
                panel = {"en": NEW_EN_PANELS, "cs": NEW_CS_PANELS}[lang][slug]
            new = render(lang, slug, template, panel)
            if old != new:
                changed.append(path)
                if not check:
                    path.write_text(new, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate Grimwild sheet HTML.")
    parser.add_argument("--check", action="store_true", help="fail if generated HTML differs")
    parser.add_argument("--lang", action="append", choices=LANGS, help="language to regenerate; repeatable")
    args = parser.parse_args()

    changed = regenerate(args.check, args.lang or list(LANGS))
    if args.check and changed:
        for path in changed:
            print(path.relative_to(ROOT))
        return 1
    if not args.check:
        print(f"updated {len(changed)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
