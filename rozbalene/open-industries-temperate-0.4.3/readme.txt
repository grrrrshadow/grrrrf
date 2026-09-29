Open Industries: Temperate
Version 0.4.3

Open Industries: Temperate is a complete Temperate economy replacement for
OpenTTD 15.3 and newer. It provides 28 cargoes, 28 industries, 14 stockpiled
processing chains, three cargo-accepting town buildings, service-responsive
primary production, 13 original industry layouts, 15 custom 8bpp industry
designs, and complete English and German interfaces.

The set adds no vehicles. New cargoes use cargo labels, classes, and capacity
multipliers so suitable base-game and NewGRF vehicles can carry them through
the normal refit interface.

INSTALLATION

Download the set through OpenTTD's Online Content window. Open NewGRF Settings,
add Open Industries: Temperate, and start a new Temperate game.

Do not combine this set with another cargo or industry economy replacement.
Place it after graphics-only sets and before vehicle sets that inspect cargo
labels. Enable it before creating a game; an existing save cannot safely be
converted to or from a replacement economy.

PLAYING

Primary industries produce without supplies. Delivering Engineering Supplies
or Fuel can boost their next production cycle. Processing industries keep
incomplete deliveries in stockpiles and run complete recipe batches when cargo
arrives. Industry-window text shows recipes, production, service, bonuses,
waiting inputs, and output awaiting pickup.

Version 0.4.3 uses full vanilla layouts for the 13 original industries. The
other 15 use revised, transparent, base-game-style artwork without artificial
terrain plates. The build normalises their scale, converts them to the OpenTTD
8bpp palette, aligns each site to its real four-by-four footprint, and assigns
each 64-pixel-wide piece to its physical map tile so camera movement and nearby
trees cannot hide fragments. The Food Market, Department Store, and Office
Building use their supplied custom artwork.
The German translation covers cargo quantities, recipes, roles, bonuses,
status messages, parameters, and town destinations.

When buying a vehicle, open its refit window and select the required cargo.
Typical matches are open or hopper vehicles for bulk cargo, tankers for
liquids, refrigerated or express vehicles for Meat and Food, and covered or
flatbed vehicles for piece goods.

COMPATIBILITY

Minimum OpenTTD: 15.3
Climate: Temperate
GRFID: OIT1
License: GNU General Public License version 2 only

SOURCE CODE AND DOCUMENTATION

The complete corresponding source code, graphics, build instructions, credits,
economy documentation, and balance report are publicly available at:

https://github.com/DuNeSliM/OpenIdustries

Project direction and economy design: Miguel
Implementation, new-cargo icons, town-building pixel art, palette conversion,
and NewGRF artwork integration: created for this project with OpenAI Codex.
Retained vanilla cargoes use icons from the active base graphics set. Initial
industry concepts were supplied by Miguel; the revised custom sources were
generated with OpenAI image generation from those concepts and the project's
style brief. OpenTTD, NML, OpenGFX, and OpenGFX2 are separate projects and do
not endorse this NewGRF.
