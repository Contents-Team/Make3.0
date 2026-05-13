Make Asset Naming Convention — [v0.5.md]
```markdown
# Make Asset Naming Convention

> **Version**: v0.5  
> **Status**: Draft  
> **Last Updated**: 2026-05-13  
> **Author**: HamIsBadass  

---

## Table of Contents

1. [Overview](#1-overview)
2. [Global Rules](#2-global-rules)
3. [Core Concepts — Source Asset vs Instance Object](#3-core-concepts--source-asset-vs-instance-object)
4. [The `v` Marker — Key Differentiator](#4-the-v-marker--key-differentiator)
5. [Naming Syntax](#5-naming-syntax)
6. [Asset Type Reference](#6-asset-type-reference)
   - [3D Model (FBX)](#61-3d-model-fbx)
   - [Image / Texture (PNG)](#62-image--texture-png)
   - [Audio (WAV / MP3)](#63-audio-wav--mp3)
   - [Video (MP4)](#64-video-mp4)
   - [Text / Font](#65-text--font)
7. [Hierarchy Rules — Parent & Child Objects](#7-hierarchy-rules--parent--child-objects)
8. [Instance Rules](#8-instance-rules)
9. [Changelog](#9-changelog)

---

## 1. Overview

This document defines the **asset naming convention** for content created with the Make program.

The goal is to satisfy two audiences simultaneously:

- **AI** — tokens must be parseable, unambiguous, and positionally stable
- **Users (creators, modelers, developers)** — names must be readable without a lookup table

### Design Principles

| Principle | Description |
|---|---|
| No spaces | Spaces break tooling and CLI pipelines |
| `_` as the only separator | No hyphens, dots, or mixed separators |
| PascalCase within tokens | `GlassBottle`, not `glassbottle` or `glass-bottle` |
| No synonyms | One agreed term per concept, no alternatives allowed |
| Minimum necessary tokens | Only include what adds meaning; remove redundant information |
| Extension = type declaration | Do not repeat type in the name when extension already declares it |

---

## 2. Global Rules

| Rule | ✅ Correct | ❌ Incorrect |
|---|---|---|
| No spaces | `GlassBottle_01` | `Glass Bottle_01` |
| Separator = `_` only | `GlassBottle_Cap_v01` | `GlassBottle-Cap-v01` |
| PascalCase per token | `BatteryPack` | `batterypack` / `battery_pack` |
| Variant = 2-digit fixed | `_01`, `_02` | `_1`, `_2`, `_001` |
| Version = `v` + 2-digit | `_v01`, `_v02` | `_V1`, `_ver01`, `_0324` |
| No redundant type token | `GlassBottle_v01.fbx` | `GlassBottle_MOD_v01.fbx` |
| English only | `BatteryPack_v01` | `배터리팩_v01` |

> ⚠️ Version history files (`_v01`, `_v02`) are for pre-delivery WIP management.  
> Final delivered assets should carry a single clean version number unless iteration tracking is explicitly required.

---

## 3. Core Concepts — Source Asset vs Instance Object

Two distinct naming layers exist in the Make pipeline:

| Layer | What it is | Where it lives | Has extension? |
|---|---|---|---|
| **Source Asset** | The original file delivered by a modeler/artist | File system / import library | ✅ Yes (`.fbx`, `.png`, etc.) |
| **Instance Object** | The object placed in a Make scene | Make scene tree | ❌ No extension |

### Why the distinction matters

The same `GlassBottle_v01.fbx` source asset can be placed into a scene **multiple times**  
as separate independent objects. Each placement is an **instance** — it has its own name,  
transform, and potentially its own animation event assigned by AI.

```

Source Asset (file):    GlassBottle_v01.fbx      ← 1 file exists

↓

Scene Instance 1:       GlassBottle_01           ← placed once

Scene Instance 2:       GlassBottle_02           ← placed again

Scene Instance 3:       GlassBottle_Open_01      ← different state variant

```

---

## 4. The `v` Marker — Key Differentiator

The `v` prefix on the variant number is the **single most important rule** in this convention.  
It is the only signal needed to distinguish a source file from a scene object.

| Pattern | Meaning |
|---|---|
| `Name_vNN.ext` | Source Asset (original file) |
| `Name_NN` | Scene Instance Object (no extension) |

```

GlassBottle_v01.fbx    ✅ Source Asset   — version 1 of the original file

GlassBottle_01         ✅ Scene Instance — 1st placement of GlassBottle in scene

GlassBottle_01.fbx     ❌ Ambiguous      — source file or misnamed instance?

GlassBottle_v01        ❌ Ambiguous      — looks like source asset but has no extension

```

---

## 5. Naming Syntax

### Source Asset

```

<Name>*[State*]v<NN>.<ext>

```

### Source Asset — Child Part

```

<ParentName>*<ChildName>*[State_]v<NN>.<ext>

```

### Scene Instance

```

<Name>*[State*]<NN>

```

### Scene Instance — Child Object (scene tree readable by AI)

```

<ChildName>_<NN>

```

### Scene Instance — Child Object (scene tree NOT readable by AI)

```

<RootInstanceName>*<ChildName>*<NN>

```

### Token Definitions

| Token | Description | Format |
|---|---|---|
| `Name` | Unique identifier of the asset | PascalCase |
| `ParentName` | Parent object's name (for child parts) | PascalCase |
| `ChildName` | The part / component name | PascalCase |
| `State` | Shape variant — only when different from base form | PascalCase (`Open`, `Broken`, `Closed`, `Damaged`) |
| `v<NN>` | Source asset version number | `v01`, `v02` |
| `<NN>` | Instance number or part variant number | `01`, `02` |

> `[State_]` is optional. Include only when the asset differs in form from the base model.

---

## 6. Asset Type Reference

### 6.1 3D Model (FBX)

File extension `.fbx` declares the type. **No type token in the name.**

#### Syntax

```

<Name>_v<NN>.fbx                          Parent model

<ParentName>_<ChildName>_v<NN>.fbx        Child part (separated delivery)

<Name>_<State>_v<NN>.fbx                  State variant

```

#### Examples

```

GlassBottle_v01.fbx

GlassBottle_v02.fbx

GlassBottle_Open_v01.fbx

GlassBottle_Broken_v01.fbx

GlassBottle_Cap_v01.fbx

GlassBottle_Label_v01.fbx

BatteryPack_v01.fbx

BatteryPack_TopCover_v01.fbx

BatteryPack_Handle_v01.fbx

WorkshopTable_v01.fbx

WorkshopTable_Drawer_v01.fbx

```

---

### 6.2 Image / Texture (PNG)

PNG is the **only file type that requires a Role/Descriptor token**.  
PNG is used for both **UI sprites** and **3D textures** — the extension alone does not declare the purpose.

#### Role / Descriptor Tokens

| Token | Meaning | Used for |
|---|---|---|
| `Sprite` | UI image (button, icon, panel, background) | UI |
| `ALB` | Albedo / Base Color | 3D Texture |
| `NRM` | Normal Map | 3D Texture |
| `RGH` | Roughness Map | 3D Texture |
| `MET` | Metallic Map | 3D Texture |
| `EMI` | Emission Map | 3D Texture |
| `MSK` | Mask Map | 3D Texture |
| `AO` | Ambient Occlusion | 3D Texture |

#### Syntax

```

<Name>*<Role>*<NN>.png              3D texture

<UIElementName>*Sprite*<NN>.png     UI sprite

```

#### Examples

```

GlassBottle_ALB_01.png

GlassBottle_NRM_01.png

GlassBottle_RGH_01.png

GlassBottle_MET_01.png

GlassBottle_Cap_ALB_01.png

BatteryPack_ALB_01.png

BatteryPack_EMI_01.png

PlayBtn_Sprite_01.png

CloseBtn_Sprite_01.png

WarningIcon_Sprite_01.png

StepCompleteIcon_Sprite_01.png

PanelBackground_Sprite_01.png

```

> ⚠️ PNG textures do **not** use `v<NN>` — they are art assets, not versioned source files.  
> Variant number `<NN>` alone is sufficient.

---

### 6.3 Audio (WAV / MP3)

Extension declares type. **No type token needed.**  
Audio category is embedded as a prefix within the `Name` token.

#### Category Prefixes

| Prefix | Meaning |
|---|---|
| `BGM` | Background Music |
| `SFX` | Sound Effect |
| `VO` | Voice Over / Narration |
| `AMB` | Ambient Sound |

#### Syntax

```

<CategoryPrefix><Description>_<NN>.<ext>

```

> No separator between category prefix and description — both are part of the single `Name` token.

#### Examples

```

BGMTutorial_01.wav

BGMBoss_01.wav

SFXUIClick_01.wav

SFXStepComplete_01.wav

SFXAlertWarning_01.wav

VONarrationIntro_01.wav

VOStep01Guide_01.wav

AMBForestNight_01.wav

AMBWorkshop_01.wav

```

---

### 6.4 Video (MP4)

Extension declares type. **No type token needed.**  
Context is embedded as a prefix within the `Name` token.

#### Context Prefixes

| Prefix | Meaning |
|---|---|
| `CUT` | Cutscene |
| `TUT` | Tutorial / Step guide |
| `LOOP` | Looping background video |
| `INTRO` | Intro sequence |
| `OUTRO` | Outro sequence |

#### Syntax

```

<ContextPrefix><Description>_<NN>.mp4

```

#### Examples

```

INTROMain_[01.mp](http://01.mp)4

OUTROCredit_[01.mp](http://01.mp)4

CUTAssemblyStep01_[01.mp](http://01.mp)4

TUTBatterySwapStep01_[01.mp](http://01.mp)4

TUTBatterySwapStep02_[01.mp](http://01.mp)4

LOOPWorkshopBackground_[01.mp](http://01.mp)4

```

---

### 6.5 Text / Font

Font files are shared resources — not content-specific.  
In-content text objects (labels, titles) are scene objects, not files.

#### Source Asset (Font File)

```

<FontFamilyName>*<Weight>*<NN>.<ext>

```

```

NotoSansKR_Regular_01.ttf

NotoSansKR_Bold_01.ttf

Roboto_Medium_01.ttf

```

#### Scene Text Object (Instance)

Follows the standard Scene Instance rule — no file extension.

```

StepTitle_01

WarningLabel_01

DescriptionBody_01

```

---

## 7. Hierarchy Rules — Parent & Child Objects

### 7.1 Source Asset Delivery

Child parts delivered as separate FBX files **must include the parent name**  
so that AI and humans can identify the relationship from the filename alone.

```

GlassBottle_v01.fbx          ← Parent

GlassBottle_Cap_v01.fbx      ← Child part of GlassBottle

GlassBottle_Label_v01.fbx    ← Child part of GlassBottle

```

### 7.2 Scene Object Hierarchy

Two cases depending on whether the AI can access the scene tree:

#### Case A — Scene tree is readable by AI

Child object names are short. The tree provides parent context.

```

GlassBottle_01               ← Root instance

Cap_01                     ← Child (parent context provided by tree)

Label_01                   ← Child

```

#### Case B — Scene tree is NOT readable by AI

Child object names embed the root instance name for full self-description.

```

GlassBottle_01               ← Root instance

GlassBottle_01_Cap_01      ← Child (parent name embedded in child name)

GlassBottle_01_Label_01    ← Child

```

| | Case A | Case B |
|---|---|---|
| Child name format | `ChildName_NN` | `RootInstance_ChildName_NN` |
| Name length | Short | Long |
| Self-describing | ❌ Requires tree | ✅ Name alone is complete |
| AI animation targeting | Requires tree context | Name only is sufficient |
| Maintenance | Parent rename has no effect on child | Parent rename requires updating all children |
| Recommended for | Make internal operation | File delivery / external review |

> **Make 3.0 note**: Apply Case A if the AI animation event system reads the scene tree as context.  
> Apply Case B if AI receives only the object name string as input.

---

## 8. Instance Rules

### Same source, multiple placements

```

Source:   GlassBottle_v01.fbx

Scene:    GlassBottle_01     ← 1st instance

GlassBottle_02     ← 2nd instance

GlassBottle_03     ← 3rd instance

```

### Different state variants, multiple placements

```

Source (base):      GlassBottle_v01.fbx

Source (open lid):  GlassBottle_Open_v01.fbx

Scene:    GlassBottle_01          ← base, 1st placement

GlassBottle_02          ← base, 2nd placement

GlassBottle_Open_01     ← open lid, 1st placement

GlassBottle_Open_02     ← open lid, 2nd placement

```

### Collision check — instance number vs source version

| Name | Layer | Meaning |
|---|---|---|
| `GlassBottle_v01.fbx` | Source Asset | Version 1 of the original file |
| `GlassBottle_v02.fbx` | Source Asset | Version 2 — revised delivery |
| `GlassBottle_01` | Scene Instance | 1st placement in scene |
| `GlassBottle_02` | Scene Instance | 2nd placement in scene |

> The `v` marker fully separates source and instance layers. **No naming collision is possible.**

---

## 9. Changelog

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-05-13 | Initial research — Unity/Unreal naming convention survey |
| v0.2 | 2026-05-13 | AI-friendly vs user-friendly naming comparative analysis |
| v0.3 | 2026-05-13 | Make-specific asset structure analysis (`.mars` / ARES Importer format) |
| v0.4 | 2026-05-13 | Domain token removed; JSON metadata excluded from scope; PNG Role/Descriptor defined; Parent-Child hierarchy rules added |
| v0.5 | 2026-05-13 | Source Asset vs Instance Object layer separation finalized; `v` marker established as key differentiator; State variant token defined; Instance naming simplified (no `_Inst` keyword); Per-type naming rules formalized for 3D / PNG / Audio / Video / Text |
```