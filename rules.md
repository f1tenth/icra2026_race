---
title: Roboracer Rules
layout: page
section: race
---

<style>
.post ol {
  list-style-type: lower-alpha;
}

.post ol ol,
.post ul ol {
  list-style-type: lower-roman;
}
.post ol, .post ul, .post p {
  margin-bottom: 0rem;
}
h2, h3, h4, h5, h6 {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>

[comment]: <> (NEW RACE CHANGE HERE)
These rules are prepared for the _24th International Roboracer Autonomous
Racing Competition_. Rules are subject to change. The latest version
can be found [here](http://icra2025-race.roboracer.ai/rules.html).

Date: 2025-02-03

**Table of content**
- ToC
{:toc}


# 1. General

International Roboracer Autonomous Racing Competition is an autonomuos vehicle racing competition open to teams of all levels. Competing teams may consist of any number of members; however, each participant should be a member of only one team.

The competition is organized as an in-person competition.

Teams can register for the competition using a [registration form](https://forms.gle/S13buonfEA4VgzHN8).

The preferred communication method with the organizers is the _#ICRA2025_ channel on [Roboracer-teams Slack](https://join.slack.com/t/robo-racer/shared_invite/zt-2sfu4qr7p-3oe27mCnH98muwRR9uEAbg).


# 2. In-person (physical) competition

1. The competition will comprise three parts – *Inspection and Orientation*, *Time
Trials* and *Vehicle Head-to-Head* race. Every participant must pass
qualification and will be automatically registered to both races.

2. Teams registered for the in-person competition need to provide and build a Roboracer car by themselves according to the constraints listed below. In addition, each team must have a unique vehicle (i.e., a research lab may not field six teams with one car). 

    * Teams may bring in spare parts including a full spare car, but only one car can be on the track at a time.
    * The spare car must also pass the inspection before it can be used in the competition.
    * If the car's engine, battery, lidar, or chassis is replaced, the team must report to the race stewards for re-inspection.
    * If a team has more than one car on the track at a time, the team will be flagged. 
    * If a team is flagged three times, the team will be disqualified from the competition.

3. Should a single lab wish to participate with multiple teams, the lab must provide a unique vehicle for each team. There are no limiations on the number of teams a lab can field as long as the following rules are followed:
    * As this is an open-source community where collaboration is encouraged, the teams are allowed to help and collaborate **before** the competition. However, during the competition, the teams must compete as independent teams.
    * Each team must run their own unique algorithms and cannot run the same code on multiple vehicles.
    * The teams may share maps, but may not share hyperparameters or other algorithmic details. The teams must compete as if they are independent teams.
    * The teams may share hardware, tools, and spare parts, as long as each team has its own unique vehicle. 
    * If a team is disqualified or eliminated for any reason, the team's members will not be allowed to join another team for the remainder of the competition.
    * Other teams are allowed to report a team that is not following these rules to the organizers.
    * If a team is flagged three times for not following these rules, the team will be disqualified from the competition.
    * If a team achieves a podium finish, only that team's members will earn the certificates and any other prizes. 

4. To qualify for the in-person competition, teams should submit a video of their car driving autonomously around a track. The video should be at least 1 minute long and show the car driving around the track without any human intervention. The video should be submitted to the organizers by the deadline listed in the timeline page.

5. To increase the quality of the future Roboracer competitions, the top 3 teams of each race are encouraged to publish the code of their algorithm under an open-source license in the [Roboracer repository](https://github.com/f1tenth) on Github.

6. In order to minimize crowding inside the racetrack, all teams should have **at most 4 team members** present at the race space during the event. Teams with more than 4 members will be required to either register as separate teams or discard/cycle their members during the event. There are no restrictions on the number of team members otherwise and all members will receive certificates of participation.
    1. Definition - Race space: The racetrack and its interior and boundaries. This includes any internal space that the competitors can stand in and any space immediately surrounding the racetrack.
    2. Teams will not be penalized for having more than 4 members in the seating and table area, as long as the members are not inside the racetrack. However, teams with more than 4 members are not guaranteed to get enough seating and table space for all members.
    3. Exceptions may be made in brief instances for the purpose of repairs or other necessary tasks.


7. Teams should not display any national flags or national symbols. This competition is between peers, not nations.

## 2.1 Vehicle Specifications

Only cars that meet the following constraints will be allowed to participate:

  1. The vehicle is constructed according to the official [bill of materials](https://f1tenth.readthedocs.io/en/foxy_test/getting_started/build_car/bom.html#bill-of-materials). The teams are allowed to use components of similar or lower specifications.
  2. Each vehicle will be inspected as a part of qualification whether it meets the criteria. In case the criteria are not met, the vehicle is disqualified.
  3. _Chassis_:
      The race is designed with **1:10 Traxxas** chassis in mind (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4platinum), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)). These chassis are recommended, but generally, any chassis within 15% of the traxxass cars' dimensions is allowed ( 238mm ≤ Width ≤ 341mm, 454 mm ≤ Length ≤ 654mm). Both 4WD and 2WD are permitted.
  4. _Main Computation Unit_:
      Due to supply chain issues, we're removing constraints on the main computation unit. Any suitable computing unit that physically fits on the vehicle within the size limit is allowed. Examples inlcude Nvidia Jetson Xavier NX, Nvidia Jetson Orin Nano, Nvidia Jetson TX2, Nvidia Jetson Nano, Intel NUC, Raspberry Pi, etc. In the spirit of the competition, all computation must be done onboard the vehicle.
  5. _LiDAR_:
      [**Hokuyo UST-30LX**](https://www.hokuyo-aut.jp/search/single.php?serial=233), its equivalent, or anything of lower specifications is allowed. The main observed characteristics are: detection range (30 m), scanning frequency (40 Hz), and angular resolution (0.125°).
  6. _Camera_:
      Both *monocamera* (e.g. Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and *stereocameras* (e.g. Intel Realsense, ZED) are allowed.
  7. _Engine_:
      Only brushless DC motors are allowed. The [**Velineon 3500 kV**](https://traxxas.com/sites/default/files/3351-INST-KC1682%20Velineon%203500_ML_120813.pdf), its equivalent, or anything of lower specifications regarding power and torque are allowed. The car must have **only one** DC motor driving the wheels. The motor could either be sensored or sensorless as long as it meets the specifications
  8.  _Other sensors_:
      Other sensors (IMUs, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g. Marvelmind) are not allowed.
  9. _Tires_:
      There are no resutrictions on the tires used by the car. Any and all tires that fit the wheels of the chassis are permitted.
  10. _Battery_:
      The drive motor should be driven *at most* by one (or any equivalent combination) battery rated at most **4s**. There are no limitations on the capacity of the battery. More than one battery can be used on the car as long as only one 4s battery powers the motor. Teams are encouraged to have spare batteries to allow fast replacements in case the battery gets discharged at an inconvenient time.
  11. _Transmitter Spot_:
      The car must have a designated spot at the front-half of the car of atleast 8cm x 12cm for a transmitter. The spot should be easily accessible and nothing should be on top of the transmitter. This spot will be used for a transmitter that will be used for time-keeping. 

Additionally, during open practice and head-to-head races, the car is required to be equipped with the following:

1. The car must be equipped with front bumper made of soft material, e.g., [TRA7436](https://traxxas.com/products/parts/7436) + [TRA7437](https://traxxas.com/products/parts/7437) +  [TRA7415X](https://traxxas.com/products/parts/7415X). This solution is compatible with _Slash_. Model of _Ford Fiesta_ already has this bumper.
    1. The bumper has to be soft to minimize the damage to the opponent’s car in case of a cras.
    2. The bumper must have a minimum of 5 cm of soft material. 
    3. The bumper must be attached to the car in a way that it does not fall off at any time during the head-to-head race.
3. The car must be equipped with a rear bumper which is at least as high as the front bumper.
4. The car has to be easily perceivable by other cars' LiDARs. Therefore, the car **must occupy a space of size at least 12×12 cm at every horizontal plane between 10 to 30 cm above the ground**. Usually, this is achieved by placing a 12x12x20cm box on top of the car at the back. 
    1. The box should be made of LiDAR perceivable material (e.g., cardboard) and not be reflective.
    2. Teams may use any shape object placed at the back of the car as long as the car has a LiDAR "signature" of at least 12x12cm at every horizontal plane between 10 to 30 cm above the ground. 
    3. As long as the object results in the desired LiDAR signature, the object can have any additional aeorodynamic shapes added like fins, wings, etc.
    4. The box maybe of any color as long as it is easily perceivable by the LiDARs of the other cars.

## 2.2 Track & racing environment

The competition will take place inside [Georgia World Congress Center](https://www.gwcca.org/georgia-world-congress-center). The characteristics of the environment where the track will be built are:

1. The surface is flat and reflective. Therefore, LiDAR beams may reflect from the ground and measure the surrounding area rather than the ground. Similarly, depth cameras have problems with proper ground detection.
2. The track border is constructed from single height air ducts of 33 cm diameter. Keep in mind that **there will be gaps** between the pipes through which the LiDAR beams can pass.
3. The track can be mapped in either the training sessions on each day or in the qualification session of each team. We are providing dedicated time slots for each team to map the track. Although many teams are using SLAM or vision-based localization techniques, a dedicated **Map Creation** or **Mapping** session is provided for the teams.
4. The track will be atleast 4 car widths (120cm) wide everywhere around the track to allow for and incentivise overtaking.
5. The track will contain a mix of choke points, sharp hairpins, wide straights and extra wide corners to test the algorithms of the cars. The track borders will contain holes on parts of the track to test out the robustness of the algorithms.
6. No humans are allowed on the track at all times, except to repair the track, or to remove a stopped car.
7. Removing the car from or placing the car on the track should always be done at the border of the track from the outside.
8. If the car is not able to drive anymore, the team has to remove the car from the track as soon as possible.
9. All days of the competition will be streamed live on twitch on the [official Roboracer channel](https://www.twitch.tv/roboracer_ai). The stream will be available for the public to watch. 

## 2.3 Practice

1. There will be two practice days for the competition. The first day will be dedicated to regulated practice sessions and the second day will be dedicated to open practice sessions.

2. The dedicated time slots for the regulated practice sessions will be designated on a first-come-first-serve basis. The schedule of the sessions will be shared with the teams before the competition. Each session will be 10 minutes long.

3. The second day of practice will be open practice sessions. To limit the number of teams on the track at the same time, the teams will be split into groups. Each group will have a shared time for open practice. The groups will be assigned by the organizers. The schedule of the sessions will be shared with the teams before the competition. The length of these sessions will be determined by the number of teams. Tentatively, the sessions will be 4 hours long.

4. During shared practice sessions, if a car is stationary on the track for more than 5 minutes and the team does not remove the car, the car will be removed by the organizers and the team will be flagged for obstructing practice.

    * Other teams are allowed to report a stationary car on the track to the organizers.
    * If a team is flagged three times for obstructing practice, the team will be disqualified from the competition.

## 2.3 Inspection

1. The purpose of the Inspection is to check that the hardware of the autonomous cars meets the competition requirements and the cars are not dangerous for the environment, opponents, and people.

2. The inspection of the vehicles is done on the first day in the morning.

3. The inspection is done by the race referees.

4. The inspection has to be completed before the Time Trials and after any significant changes to the cars hardware or algorithms during any of the days of the event.

## 2.4 Time Trial

### 2.4.1 Definitions

1. *Touching* means moving the object by less than 5 cm. Moving by greater distance is called *Crashing*.

2. Moving the track border by any distance is called *Crashing*.

### 2.4.2 General

1. Each team must pass the inspection to be able to participate in the Time Trial. Any team that does not pass the inspection on the first day will be disqualified from the competition.

2. Time Trial is a race with a goal to drive through the designated track as fast as possible and as consistently as possible. The idea is to push the algorithms to their limits.

3. The race consists of two heats. Each heat lasts for 5 minutes, and the goal is to drive a single lap in as short time as possible and to drive as many complete laps as possible. Crashing and stopping the car does not pause the heat timer.

4. The heat sessions are split in two with a one one-hour practice session in between. The teams have to book a time slot in each session. The schedule of the sessions will be shared with the teams before the race.

5. Each team is provided two dedicated time slot for their vehicle to qualify. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team. There will be 1-5 minutes of dedicated time to switch from one team to the next. If a team is not able to run the car in this dedicated time slot, the qualification phase is not passed for this team.

6. The teams are allowed to change the configuration of their algorithms in between the heats, and even during the heat. When the configuration is changed during the heat, the car must stand still. In other words, the teams cannot update the configuration on-line while the car moves.

7. The map (track layout) is **known** a priori (from practice the day before) and the track layout does not change over the whole competition. Keep in mind that cars crash into the walls and the layout of the track might slightly shift a little bit. Please consider this in your algorithms.

### 2.4.3 Requirements for Time Trial qualification

1. Each vehicle must demonstrate that it can drive autonomously one lap through the track without crashing.

2. The team must demonstrate that it is possible to trigger car emergency stop remotely.

3. Each team will have two dedicated time slots of 5 minutes each to qualify, with a one-hour break in between for all teams to practice.

    1. The teams have to book a time slot in each session.
    2. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team.
    3. There will be 1-5 minutes of dedicated time to switch from one team to the next.
    4. If a team is not able to run the car in either dedicated time slots, the team fails the qualification phase and is disqualified from the competition.

### 2.4.4 Penalties

1. Touching the border of the track is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash.

2. Upon crashing the track border the team has to stop the car and move it (by hand or using the remote control) to the latest position before crash. After repairing the track, the race may continue. The time spent on moving the car to the checkpoint and repairing the track is considered the penalty.

### 2.4.5 Evaluation

Each team will be evaluated based on the following criteria:

1. *Fastest lap time*. The laptime will be measured with a time-keeping system provided by the race director.
2. *Number of consecutive uninterrupted laps*

There will be two results tables based on these criteria.

The final score for the qualification consists of two parts:

1. **Fastest laptimes**: Teams are ranked based on their fastest lap times. Points are awarded according to the ranking. For example, with 10 teams, the fastest team receives 10 points, the second fastest receives 9 points, the third fastest receives 8 points, and so on.

2. **Consecutive uninterrupted laps**: Teams are also ranked based on the number of consecutive uninterrupted laps they complete. Points are awarded similarly. For example, with 10 teams, the team with the most laps receives 10 points, the second team receives 9 points, the third team receives 8 points, and so on.

The final score is the sum of the points from both categories. Note that the best lap times and the number of laps can be achieved in different time slots. This allows teams to push their algorithms to the limits in each of the two categories.

Should a tie occur in the final ranking, the team with more laps is ranked higher.

The qualification is passed by finishing a single lap without crashing. Otherwise, the team is disqualified from the competition.

## 2.5 Head-to-Head Race

### 2.5.1 General

1. The Head-to-Head race is a race with two cars on the track at the same time.

2. The racetrack has the same layout as in the training and qualification sessions.

3. The algorithms must not intentionally hinder the opponent or perform any damage to it. Specifically, maneuvers such as deliberate crowding of a car beyond the edge of the track or any other abnormal change of direction are strictly prohibited. The referees will have the final say in whether a driver is in violation of this rule.

    * Should a team be found in violation of this rule, the referees will issue a warning in the form of a yellow flag. After three warnings, the team is disqualified.

4. The head-to-head race will be organized as a double-elimination tournament with two brackets seeded by results of the qualification.

5. The two winners of each bracket will qualify to compete in the Final Four race. This final tournament will feature a single elimination bracket.

6. Before the start of **each** head-to-head race, **both** teams will be tested for obstacle avoidance and are required to use the same code for the race. Any violations to this rule could result in disqualification of the violating team (up to the organizers).
    1. Each team has to demonstrate obstacle avoidance at race speeds using their race code unchanged. A violation to this rule is penalized and three penalties result in disqualification.
    2. The obstacle will be placed on an easy-to-detect location on the track. The goal of this test is to ensure that the autonomous agent can pass the base-case obstacle avoidance test at race speeds.
    3. Stopping before the obstacle will not be considered as a passing of the test. The car must pass the obstacle without coming to a complete stop. This is to incentivize overtaking algorithms.

7. Teams that fail to pass the obstacle avoidance test will have the option to race on the condition that they do not overtake the opponent.

    1. If the team fails to pass the obstacle avoidance test and overtakes the opponent, the team will be disqualified.
    2. The team that failed the obstacle avoidance is permitted to use manual control when the car is 5 meters behind the opponent to slow down the car and avoid overtaking.
    3. The faulty team is not allowed to use manual control to speed up the car and overtake the opponent.
    4. The faulty team can only overtake the opponent if the opponent crashes.

8. One head-to-head race consists of two teams racing against each other. One race has a dedicated timeslot of around 10 minutes. If one team is not showing up in these 10 minutes and let their car race, the other team won. If at some point along the race a car is not able to drive anymore (e.g. hardware issue, software not running etc.) and the teams are not able to restart the car withing the 10 minutes, the other team wins the race. No time extensions are given and after the 10 minutes we move on to the next time slot and the next team.
    * Each race consists of three rounds, the team that wins two rounds wins the race.

9. Both competing cars start from the same starting line used in the qualifications.

    1. The teams will start side-by-side seperated by one car width (30cm) from each other.
    2. For the first round, the team that ranked higher in qualifications chooses the starting position (left or right). The other team starts on the opposite side.
    3. In the second round, the teams switch sides. The team that started on the left side in the first round starts on the right side in the second round.
    4. Should a third round be necessary, a coin flip will determine the starting position. The team that ranked higher in qualifications will call the coin flip (i.e heads or tails). The team that wins the coin flip chooses the starting position.

10. Overtaking may be carried out on either the right or the left.

11. As opposed to time trials, no reconfiguration is allowed during the race, except after a crash, as described below.

12. Ultimately, organizers reserve the right to assign blame in the case of vehicle collision in the head-to-head tournament.

13. The race stewards will utilize a system of colored flags to communicate with the teams. The flags are as follows:

    1. **Checkered flag**: The steward holds a checkered flag in each hand, one for each team. A flag is raised if the team is on the last lap. The flag is dropped and then waved when the team finishes and wins the current round.
    2. **Red flag**: The steward holds a red flag in each hand, one for each team. A flag is raised if a race-stopping car crash occurs. The flag is dropped after all cars are stopped, and the team representatives are allowed to approach the track. After the crash is resolved by the stewards, the flag is dropped and the race resumes.
    3. **Yellow flag**: The steward holds a yellow flag in each hand, one for each team. A flag is raised if the team is warned for a rule violation.
    4. **Black flag**: The steward holds the black flag in each hand, one for each team. A flag is raised if the team is disqualified. The flag is dropped after the disqualified team stops the car and leaves the track. The opponent is allowed to continue the race till completion of the set number of laps.
    5. **Green flag**: Optional - raised to signal that the race is safe to continue. The flag is dropped after the race resumes.
    * The flag assignment is done at the start based on the qualification results. The team with the higher qualification result that starts on the right side of the track is assigned the flag set in the right hand. The team with the lower qualification result that starts on the left side of the track is assigned the flag set in the left hand.

14. Collisions are judged by the referees.
    1. Collisions with track boundaries do not stop the race. The team that crashed into the track boundary must fix the track and place the car at the location of the crash. The opponent is allowed to continue. The crashed team bears the burden of the time spent on fixing the track and placing the car.
    2. Light side-bumps and slow-speed nudges are not penalized and do not stop the race.
    3. High-impact crashes that result in the displacement of one or both cars on crash result in a stoppage of the race.
    4. If a car crashes into the opponent, the referees will judge which car is at fault.
    5. Both cars will be restarted at the location of the crash, with the at-fault car placed behind the other car by 2 meters.
    6. A crash is not considered a warning unless judged by the referees.
    7. Crashes that result in a warning include but are not limited to "malicious" crashes where the autonomous car did not attempt to slow down or steer away from the opponent.
      * Under special circumstances, the referees may decide to give a warning to a team with the option of stopping the race to address the issue. The team has a maximum of 5 minutes to fix the issue and resume the race.
    8. After 3 warnings, the team is disqualified and the opponent automatically wins.
    9. If the team that was crashed into is able to autonomously detect and recover from the crash by stopping on the side of the track, that team is granted an extra head-start of 1 meter before the restart (i.e the at-fault car is placed 3 meters behind the other car).

15. In abnormal circumstances, where a liquid spills on the track for example, the race will be stopped and any abnormal conditions are resolved before continuing the race. 
    1. Abnormal conditions are subject to the discretion of the referees. This may include but is not limited to: a car stopping on the track, a car losing a wheel, a car catching fire, a car leaking fluids, etc
    2. The race will be resumed with the cars at the location of the stoppage. No penalties are given to the teams for the stoppage, and the timer is paused during the stoppage.

### 2.5.2 Requirements for qualification

1. The team has successfully completed the Time Trial.
2. The car must be equipped with front bumper made of soft material, e.g., [TRA7436](https://traxxas.com/products/parts/7436) + [TRA7437](https://traxxas.com/products/parts/7437) +  [TRA7415X](https://traxxas.com/products/parts/7415X). This solution is compatible with _Slash_. Model of _Ford Fiesta_ already has this bumper.
    1. The bumper has to be soft to minimize the damage to the opponent’s car in case of a cras.
    2. The bumper must have a minimum of 5 cm of soft material. 
    3. The bumper must be attached to the car in a way that it does not fall off at any time during the head-to-head race.
3. The car must be equipped with a rear bumper which is at least as high as the front bumper.
4. The car has to be easily perceivable by the opponent’s LiDAR. Therefore, the car **must occupy a space of size at least 12×12 cm at every horizontal plane between 10 to 30 cm above the ground**.
5. The car needs to provide beforehand that is is able to avoid static and dynamic obstacles. This is evaluated by the race referess with a test:
   1. The cars need to run 1 lap around the racetrack that includes static and dynamic obstacles
   2. These obstacles contain of size up to 35×32×30 cm, made from LiDAR perceivable material (e.g., cardboard).
   3. The racecars must show their ability to avoid those obstacles by overtaking them. Stopping before the obstacle is not considered as a passing of the test. 
   4. Based on this results the access to the race is granted.

### 2.5.3 Penalties

1. Touching the border of the track is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash. (Same rules as for Time Trial.)

2. Touching the opponent is not penalized unless one of the cars significantly diverges from its expected trajectory.

3. Upon crashing the border of the track, the team has to fix the track and place the car on the side of the track at the place where the car first crashed the border. Then, the car can continue the race. During all of this, the opponent’s car must not be restricted by the team’s actions and the opponent is allowed to further race without stopping its car. The penalty is the time spent on fixing the track and placing the car.

4. Upon crashing the opponent, these steps are applied:

    1. Refrees call the crash and signal for it by raising the red flag.
    2. Referees judge which car is at fault.
    3. Both cars are placed at the location of the crash, with the at-fault car placed behind the other car by 2 meters.
    4. The referees restart the race with a green flag.

### 2.5.4 Evaluation

1. The first car that completes **20 laps** wins.
2. There will be at least three referees.
3. One referee will be assigned to each car and is solely responsible to call flag raises and rule violations per-team. The third referee is tasked with enforcing penalties, crash resolution, and time-keeping.

# 3. Virtual (simulation) competition

## 3.1 General
  1. The virtual competition will be completely done in an simulation environment only and no hardware is involved.

  2. This simulation environment is based on the [AutoDrive Ecosystem](https://autodrive-ecosystem.github.io/). The Roboracer virtual competition will be complete done in this environment only and teams need to submit their code in time to this platform.

  3. The virtual competition will comprise two parts – *Time Trials* and *2 Vehicle Head-to-Head* race. Every participant must pass the Time Trials and will be automatically registered to both races.

  4. Roboracer reserves the right to reject any submission that we deem illegal due to circumstances such as exploiting the simulation environment. Therefore their source code submission will be examined by the race stuarts after the race.

  5. The map used for all the races (Time Trials, Head-to-Head) will be the same. In the Time Trials no obstacles will be present on the map. Obstacles will only be used before head-to-head races to test the obstacle avoidance capabilities of the cars.

  6. All details will be posted on the official page for the virtual competition [here](https://autodrive-ecosystem.github.io/competitions/roboracer-sim-racing-icra-2025/#f1tenth-sim-racing-league-icra-2025).

<!-- ## 3.2 Registration, Training, Code Submission.

2. Teams must register themselves for the 24th Roboracer Autonomous Racing Competition on the Riders.Ai platform on their own with their team name.

3. We will provide test environments (maps) for the teams to use this platform as a training and evaluation environment while they develop their code.

4. Teams need to prepare their code with their local machine.

5. Teams need to submit their code with their local machine.

6. All simulation event evaluations are done on the Riders.Ai cloud. Based on this evaluation the leaderboard will be created.

7. We define deadlines for the submissions of the Time-Trial code and the Head-to-Head for the teams. No extensions are given.

## 3.3 Time Trials

1. The Time Trials in the Roboracer simulation environment are here to define both the capabilities of the vehicles to race in a static environment with and without obstacles as well as for creation of the seeding in the Head-to-Head race.

2. The Time Trials are single vehicle races only.

3. The Time Trials consist of 2 races:

  1. **Qualification** race: Race 2 laps of track as quickly as possible without collision into the walls (determines Racing Competition seeding). If an agent can finish without collision with the environment, it’ll receive a lap time and update its ranking on the leaderboard.

  2. **Obstacle avoidance** race: Race 2 laps around the track with added obstacles unknown to participants. The car needs to go round 2 laps without collision. The location and the size of the obstacles will not be revealed prior to submission. Some example maps with obstacles will be provided.

4. The submission of the Time Trial Code is done via the Riders.ai platform

5. The code for both Qualification and Obstacle avoidance race needs to be the same.

## 3.4 Head To Head Race

1. The Head-to-Head race is a race with two cars on the track at the same time.

2. The car that crosses the finish line first after 2 laps wins the race.

3. The Head-to-Head race is a best of 3 trials. The car that wins two races moves on to the next round.

  1. The third race is a tie-braker if the first two races are 1:1. In the third race, the cars starting again on their predifined P1 and P2 position. The car that is seeded in the qualification higher is located on P1.

4. The cars start in alternating position (inside, outside) in each of the races.

5. Seeding: The elimination bracket of the tournament will be filled by submissions that passed the obstacle avoidance test and seeded by the result of the timed trials. For example, with 8 teams, the bracket of the first round will be (#1 vs. #8, #2 vs. #7, #3 vs. #6, and #4 vs. #5).

6. Overtaking: According to the circumstances, may be carried out on either the right or the left. Maneuvers liable to hinder other drivers, such as deliberate crowding of a car beyond the edge of the track or any other abnormal change of direction, are strictly prohibited. The stewards will have the final say in whether a driver is in violation of the rule.

7. Causing a collision (decided by the stewards) for more than 3 times will result in automatic disqualification of one car.

8. Collisions at the fault of both vehicles will result in a redo trial. After 3 redos of the same case, both vehicles are disqualified.

9. The stewards reserve the right to have the final say. -->
