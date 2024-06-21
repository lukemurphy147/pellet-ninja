# Software Requirements

# Specification

## for

# Pellet Knight

#### Version 0.

#### Prepared by Jordan Coats

#### P2_T: Tatiana Almonacy (100641150) , Johnathan Buchanan

#### (100610406) , Jordan Coats (100671756) , Evan Mowry (100659620) ,

#### Luke Murphy (100642581)

#### 2/10/


## Software Requirements Specification for <Project> Page ii

## Table of Contents

Table of Contents...........................................................................................................................ii

## Revision History

- 1. Introduction.............................................................................................................................. Revision History.............................................................................................................................ii
      - 1.1 Purpose.......................................................................................................................................
      - 1.2 Document Conventions..............................................................................................................
      - 1.3 Project Scope..............................................................................................................................
      - 1.4 References..................................................................................................................................
- 2. Overall Description..................................................................................................................
      - 2.1 Product Perspective....................................................................................................................
      - 2.2 User Classes and Characteristics................................................................................................
      - 2.3 Operating Environment..............................................................................................................
      - 2.4 Design and Implementation Constraints.....................................................................................
      - 2.5 Assumptions and Dependencies.................................................................................................
- 3. System Features.......................................................................................................................
      - 3.1 System Feature 1........................................................................................................................
      - 3.2 System Feature 2 (and so on)......................................................................................................
- 4. Data Requirements..................................................................................................................
      - 4.1 Logical Data Model....................................................................................................................
      - 4.2 Data Dictionary..........................................................................................................................
      - 4.3 Reports.......................................................................................................................................
      - 4.4 Data Acquisition, Integrity, Retention, and Disposal..................................................................
- 5. External Interface Requirements...........................................................................................
      - 5.1 User Interfaces............................................................................................................................
      - 5.2 Software Interfaces.....................................................................................................................
      - 5.3 Hardware Interfaces....................................................................................................................
      - 5.4 Communications Interfaces........................................................................................................
- 6. Quality Attributes....................................................................................................................
      - 6.1 Usability.....................................................................................................................................
      - 6.2 Performance...............................................................................................................................
      - 6.3 Security......................................................................................................................................
      - 6.4 Safety..........................................................................................................................................
      - 6.5 [Others as relevant].....................................................................................................................
- 7. Internationalization and Localization Requirements...........................................................
- 8. Other Requirements................................................................................................................
- Appendix A: Glossary....................................................................................................................
- Appendix B: Analysis Models.......................................................................................................
   - Jordan Coats 2/10/20 Project Start 0. Name Date Reason For Changes Version


## Introduction

#### 1.1 Purpose.......................................................................................................................................

This SRS describes the game’s functional and nonfunctional requirements for Pellet Knight.

#### 1.2 Document Conventions..............................................................................................................

No document conventions are being used in this version.

#### 1.3 Project Scope..............................................................................................................................

This specification establishes the functional, performance, and development requirements for the
first release of Pellet Knight.

#### 1.4 References..................................................................................................................................

**2D** Two dimensional, eg sprite based instead of polygonal based.
**Platformer** Genre where the character progresses a mostly linear level via jumping
**NES** Nintendo Entertainment System

## 2. Overall Description..................................................................................................................

#### 2.1 Product Perspective....................................................................................................................

Pellet Knight is a new 2D platformer game. While it is it’s own entry in this genre it will heavily
borrow elements from past series such as Super Mario Bros., Mega Man, and Castlevania. The
style of the game is based off of video games from the Nintendo Entertainment System era and we
will mimic the mindset and flow of games from that era as close as possible.

#### 2.2 User Classes and Characteristic

The target audience for Pellet Knight is any fans of older NES era platformer games looking to
relive the fun that they might have experienced in the past or new users being introduced to the
genre.

#### 2.3 Operating Environment..............................................................................................................

The game will be capable of running on most machines that have the ability to use Python.


#### 2.4 Design and Implementation Constraint

While an easy language to use Python may not be the best language as it is slower than
languages like C and may struggle with rendering 3D we believe that we can overcome some of
these limitations by staying within the NES era to keep it simple.

#### 2.5 Assumptions and Dependencies.................................................................................................

_<List any assumed factors (as opposed to known facts) that could affect the requirements stated in
the SRS. These could include third-party or commercial components that you plan to use, reuse
expectations, issues around the development or operating environment, or constraints. The project
could be affected if these assumptions are incorrect, are not shared, or change. Also identify any
dependencies the project has on external factors outside its control.>_

## 3.System Features

3.1 Playable Character
3.2.1	Description
The game will have a playable character that allows the user to interact with the levels, enemies and bosses. This character will be able to move left to right, jump and shoot. They will also have health and be able to take damage and die if their health is reduced to zero.
3.1.2	Stimulus/Response Sequences
3.1.2.1
	Stimuli:		- user presses direction left or right
	Response:	- playable characters x positions shift in that direction restrained by the level. 
	

3.2 Playable Character Jump
3.2.1	Description
The user/player can make the playable character jump. This jump will move the playable character up on the screen until the character reaches a peak y coordinate or collides with an object, that character then will fall down. This will  allow the character to traverse the level’s obstacles. Priority = high

3.2.2	Stimulus/Response Sequences
3.2.2.1
Stimulus:	User only presses the jump button
	Response:	The playable character moves straight up in the scene
3.2.2.2
	Stimulus:	User presses the jump button with a direction left or right button.
	Response:	The playable character will move across the scene in a quadratic shape.
3.2.3Functional Requirements
<Itemize the specific functional requirements associated with this feature. These are the software capabilities that must be implemented for the user to carry out the feature's services or to perform a use case. Describe how the product should respond to anticipated error conditions. Use “TBD” as a placeholder to indicate when necessary information is not yet available.>
3.3 Levels

3.3.1	Description
The levels are the collection of platforms for the player to land on when jumping, pits to kill the playable character and walls/restrictions of movement for all characters. Platforms and pits occupy a space within the level. players can land on the platform to climb.
3.3.2	Stimulus/Response Sequences
3.3.2.1
Stimulus:	Playable character occupies a pit
	Response:	Playable character is brought back to the beginning of the level.
3.3.2.2
	Stimulus:	Playable character reaches the end of the level
	Response:	The game will move on to the next level.
3.3.2.3
	Stimulus:	Playable character reaches the end of the final level
	Response:	The level will place the boss enemy here, if the boss is killed the game is over.

3.4 Boss Enemy
3.4.1 Description

There will be a “boss” enemy at the end of the game that moves and attacks based on the current location of the playable character. This boss will jump and shoots pellets towards the current location of the playable character. This boss will have a set “health” of 3 ticks. When the playable characters successfully shoots the boss it will lose a health tick. When the boss runs out of ticks it will die. Priority = High.
3.4.2 Stimuli and response

	3.4.2.1
	Stimuli:		Playable character successfully shoots the boss with a pellet
	Response:	Boss loses one tick of health
	
	3.4.2.2
	Stimuli:		Playable character occupies a space nearby boss
	Response:	Boss jumps and shoots a pellet towards that space
	
	3.4.2.3
	Stimuli:		Boss runs out of health ticks
	Response:	Boss is removed from the game.

3.4.2.4
	Stimuli:		playable character runs out of health ticks
	Response:	the boss's health is reset and the playable character is brought to the entrance.

3.5 Damage 
3.5.1 : Description
As a player, I have to know how much damage I am taking from my enemies as I play. (Low priority) 
3.5.2 : Stimulus/Response Sequences
3.5.2.1
Stimulus:
Player gets hits by a enemy
Response:
Players loses a Health Item every time they are hit by an enemy. 
3.6 Death  
3.6.1 : Description
As a player gets hit by an enemy they lose a health item. If they lose all three health items the player dies resulting in the “game lost” screen. ( High priority) 
3.6.2 : Stimulus/Response Sequences
3.6.2.1
Stimulus: 
Enemy hits player 3 times
Response:
Player dies which results in the “game lost '' screen appearing on screen


## 4.Data Requirements

_<This section describes various aspects of the data that the system will consume as inputs,
process in some fashion, or create as outputs.>_

#### 4.1Logical Data Model

_<A data model is a visual representation of the data objects and collections the system will process
and the relationships between them. Include a data model for the business operations being
addressed by the system, or a logical representation for the data that the system itself will
manipulate. Data models are most commonly created as an entity-relationship diagram.>_

#### 4.2Data Dictionary

_<The data dictionary defines the composition of data structures and the meaning, data type,
length, format, and allowed values for the data elements that make up those structures. In many
cases, you're better off storing the data dictionary as a separate artifact, rather than embedding it
in the middle of an SRS. That also increases its reusability potential in other projects.>_

#### 4.3Reports

_<If your application will generate any reports, identify them here and describe their characteristics.
If a report must conform to a specific predefined layout you can specify that here as a constraint,
perhaps with an example. Otherwise, focus on the logical descriptions of the report content, sort
sequence, totaling levels, and so forth, deferring the detailed report layout to the design stage.>_

#### 4.4 Data Acquisition, Integrity, Retention, and Disposal..................................................................

_<If relevant, describe how data is acquired and maintained. State any requirements regarding the
need to protect the integrity of the system's data. Identify any specific techniques that are
necessary, such as backups, checkpointing, mirroring, or data accuracy verification. State policies
the system must enforce for either retaining or disposing of data, including temporary data,
metadata, residual data (such as deleted records), cached data, local copies, archives, and interim
backups.>_

## 5.External Interface Requirements

_<This section provides information to ensure that the system will communicate properly with users
and with external hardware or software elements.>_


#### 5.1User Interfaces

_<Describe the logical characteristics of each interface between the software product and the users.
This may include sample screen images, any GUI standards or product family style guides that are
to be followed, screen layout constraints, standard buttons and functions (e.g., help) that will
appear on every screen, keyboard shortcuts, error message display standards, and so on. Define
the software components for which a user interface is needed. Details of the user interface design
should be documented in a separate user interface specification.>_

#### 5.2Software Interfaces

_<Describe the connections between this product and other software components (identified by
name and version), including other applications, databases, operating systems, tools, libraries,
websites, and integrated commercial components. State the purpose, formats, and contents of the
messages, data, and control values exchanged between the software components. Specify the
mappings of input and output data between the systems and any translations that need to be made
for the data to get from one system to the other. Describe the services needed by or from external
software components and the nature of the intercomponent communications. Identify data that will
be exchanged between or shared across software components. Specify nonfunctional
requirements affecting the interface, such as service levels for responses times and frequencies,
or security controls and restrictions.>_

#### 5.3Hardware Interfaces

_<Describe the characteristics of each interface between the software and hardware (if any)
components of the system. This description might include the supported device types, the data and
control interactions between the software and the hardware, and the communication protocols to
be used. List the inputs and outputs, their formats, their valid values or ranges, and any timing
issues developers need to be aware of. If this information is extensive, consider creating a
separate interface specification document.>_

#### 5.4Communications Interfaces

_<State the requirements for any communication functions the product will use, including e-mail,
Web browser, network protocols, and electronic forms. Define any pertinent message formatting.
Specify communication security or encryption issues, data transfer rates, handshaking, and
synchronization mechanisms. State any constraints around these interfaces, such as whether e-
mail attachments are acceptable or not.>_

## 6.Quality Attributes

#### 6.1Usability

_<Specify any requirements regarding characteristics that will make the software appear to be
“user-friendly.” Usability encompasses ease of use, ease of learning; memorability; error
avoidance, handling, and recovery; efficiency of interactions; accessibility; and ergonomics.
Sometimes these can conflict with each other, as with ease of use over ease of learning. Indicate
any user interface design standards or guidelines to which the application must conform.>_


#### 6.2Performance

_<State specific performance requirements for various system operations. If different functional
requirements or features have different performance requirements, it's appropriate to specify those
performance goals right with the corresponding functional requirements, rather than collecting
them in this section.>_

#### 6.3Security

_<Specify any requirements regarding security or privacy issues that restrict access to or use of the
product. These could refer to physical, data, or software security. Security requirements often
originate in business rules, so identify any security or privacy policies or regulations to which the
product must conform. If these are documented in a business rules repository, just refer to them.>_

#### 6.4Safety

_<Specify requirements that are concerned with possible loss, damage, or harm that could result
from use of the product. Define any safeguards or actions that must be taken, as well as potentially
dangerous actions that must be prevented. Identify any safety certifications, policies, or regulations
to which the product must conform.>_

#### 6.5[Others as relevant]

_<Create a separate section in the SRS for each additional product quality attribute to describe
characteristics that will be important to either customers or developers. Possibilities include
availability, efficiency, installability, integrity, interoperability, modifiability, portability, reliability,
reusability, robustness, scalability, and verifiability. Write these to be specific, quantitative, and
verifiable. Clarify the relative priorities for various attributes, such as security over performance.>_

## 7.Internationalization and Localization Requirements

_<Internationalization and localization requirements ensure that the product will be suitable for use
in nations, cultures, and geographic locations other than those in which it was created. Such
requirements might address differences in: currency; formatting of dates, numbers, addresses, and
telephone numbers; language, including national spelling conventions within the same language
(such as American versus British English), symbols used, and character sets; given name and
family name order; time zones; international regulations and laws; cultural and political issues;
paper sizes used; weights and measures; electrical voltages and plug shapes; and many others.>_

## 8.Other Requirements

_<Examples are: legal, regulatory or financial compliance, and standards requirements;
requirements for product installation, configuration, startup, and shutdown; and logging, monitoring
and audit trail requirements. Instead of just combining these all under "Other," add any new
sections to the template that are pertinent to your project. Omit this section if all your requirements
are accommodated in other sections. >_


## Appendix A: Glossary....................................................................................................................

_<Define any specialized terms that a reader needs to know to understand the SRS, including
acronyms and abbreviations. Spell out each acronym and provide its definition. Consider building a
reusable enterprise-level glossary that spans multiple projects and incorporating by reference any
terms that pertain to this project.>_

## Appendix B: Analysis Models.......................................................................................................

_<This optional section includes or points to pertinent analysis models such as data flow diagrams,
feature trees, state-transition diagrams, or entity-relationship diagrams. You might prefer to insert
certain models into the relevant sections of the specification instead of collecting them at the end.>_


