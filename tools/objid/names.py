import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
# type: (name, category, guess?)
S,P,E,B,N,H,M,D,X='Start & exits','Pickups','Enemies','Bosses','Characters','Hazards','Platforms & gadgets','Scenery','Bonus levels'
NAMES={
0:('Start / door',S,0),
60:('Level exit (invisible)',S,0),
61:('Doorway (invisible)',S,1),
9:('Seaweed',D,0),10:('Bubbles',D,0),11:('Blue coral',D,0),12:('Little red fish',D,0),
13:('Pink kelp curl',D,0),14:('Small pink kelp curl',D,0),15:('Red tube coral',D,0),16:('Orange tube coral',D,0),
17:('Red branch coral',D,0),18:('Pink crystal',D,0),19:('Bubble puff',D,1),20:('Bubble puff (B)',D,1),21:('Bubble puff (C)',D,1),
22:('Green kelp curl',D,0),23:('Tall pink kelp curl',D,0),24:('Golden dome',D,1),25:('Monitor screen',D,0),
26:('Orange coral',D,0),27:('Red coral',D,0),29:('Monitor screen (small)',D,0),36:('Water fountain',D,1),
111:('Little yellow fish',D,1),112:('Glowing orb',D,1),
30:('Gold key',P,0),31:('Extra life',P,0),32:('Underwear (health)',P,0),33:('Krabby Patty',P,0),34:('Golden spatula',P,0),35:('Silver key',P,0),
37:('Robot (walker)',E,0),38:('Robot (walker B)',E,0),39:('Robot (flyer)',E,0),40:('Robot (walker C)',E,0),41:('Umbrella robot',E,0),
42:('Blue octopus',E,0),43:('Spiky red crab',E,0),44:('Spiky red puffer',E,0),45:('Spiky red puffer (B)',E,0),
46:('Pink jellyfish',E,0),47:('Pink jellyfish (B)',E,0),48:('Red clam',E,0),49:('Red clam (B)',E,0),50:('Red clam (C)',E,0),
51:('Diver robot',E,0),52:('Cone-head robot',E,0),53:('Diver robot (B)',E,0),54:('Electric spark (small)',H,1),
55:('Cannon robot',E,0),56:('Cannon robot (B)',E,0),57:('Cone-head robot (B)',E,0),58:('Purple bubble',E,1),
66:('Orange mini-sub',E,0),67:('Green mini-sub',E,0),70:('Propeller robot',E,0),71:('Propeller robot (B)',E,0),
72:('Ceiling claw',E,0),73:('Ceiling claw (B)',E,0),74:('Ceiling claw (C)',E,0),75:('Ceiling claw (D)',E,0),
76:('Flying fish',E,0),78:('Flying fish (B)',E,0),79:('Purple hover-boat',E,1),114:('Ceiling eye',E,1),
82:('Sandy',N,0),83:('Squidward',N,0),84:('Mr. Krabs',N,0),85:('Patrick',N,0),86:('Gary',N,0),
87:('Green fish citizen',N,0),88:('Pink fish citizen',N,0),89:('Mermaid Man',N,0),90:('Fish citizen (red shirt)',N,0),91:('Mystery the seahorse',N,0),
94:('Boss: Star Power',B,0),95:('Boss: Robo-Sandy',B,0),96:('Boss: Robo-Squidward',B,0),97:('Boss: SpongeBot SteelPants',B,0),98:('SpongeBot boss: press',B,1),
77:('Flame arm',H,0),99:('Spiked pillar',H,0),104:('Electric beam',H,0),110:('Electric spark',H,0),113:('Piston crusher',H,1),
59:('Bounce pad',M,0),63:('Purple block',M,1),64:('Flower block',M,1),65:('Purple block (small)',M,1),
68:('Bouncy umbrella (red)',M,0),69:('Bouncy umbrella (green)',M,0),80:('Arrow block',M,0),81:('Arrow block (small)',M,0),
100:('Spatula gate',M,0),101:('Jelly block (outline)',M,1),102:('Jelly block (solid)',M,1),103:('Screw platform',M,0),
105:('Light pole',M,1),106:('Floor button',M,1),107:('Floor button (B)',M,1),108:('Jelly switch',M,1),109:('Lever',M,1),115:('Conveyor platform',M,1),
28:('Finish line',X,0),62:('Finish trigger (invisible)',X,1),92:('Vehicle start (unicycle levels)',X,1),93:('Vehicle start (bath/boat levels)',X,1),
}
CATS=[S,P,E,B,N,H,M,D,X]
