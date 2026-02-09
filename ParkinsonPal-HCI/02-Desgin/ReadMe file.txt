ParkinsonPal – HCI Project (Group08)
Figma Link:
https://www.figma.com/design/E0L2XanMxAwUJDKOXBzMUB/ParkinsonPal?node-id=0-1&p=f&t=jUPIMxbNXoE5ig7E-0 
________________


Screen Flow & Navigation
Home Screen Access
The home screen acts as the central hub. It links directly to:
* Track Your Symptoms

* Medication Manager

* Exercise & Therapy

* Brain Games

 Vertical Flows (Fully Implemented)
   1. Register

   2. Sign In

   3. Register (Urdu)

   4. Sign In (Urdu)

   5. Track Your Symptoms

   6. Medication Manager

   7. Exercise & Therapy

   8. Brain Games

Horizontal Flows
      * Download button under:

         * Track Your Symptoms → Symptom History

         * Medication Manager → Track Medicines

            * Settings

            * Profile

            * Accessibility Settings
(Redirects to in-built phone settings; supports both English and Urdu)

________________


 Major Design Decisions
General
               * Added Home button to all screens for ease of navigation

               * Retained Back button to support familiar mental models

               * Minimized scrolling to accommodate tremors and age-related dexterity issues

               * Used inbuilt accessibility features (e.g., voice typing via system keyboards) instead of building new ones

________________


Register & Sign-In
                  * Required for data privacy and personalization purposes

                  * Used phone number instead of email (as it's more common among elderly in Pakistan/South Asia)

                  * Used dropdowns for DOB, diagnosis date, gender, as it is easier to select than type

                  * Urdu and English versions created for inclusivity

________________


Track Your Symptoms
                     * Used emoji-based rating scales (color-coded) for easy recognition and interaction

                     * Ratings visually map onto calendar-based symptom history, allowing users to see a color-coded overview of daily well-being

                     * Avoided open-ended input except for "Anything Else" section.
                     * “Anything Else” to allow users to track anything that the current tracker has missed. 

________________


Medication Manager
                        * Renamed from Medication Scheduler to Medication Manager for broader clarity

                        * Divided into:

                           * Create Schedule

                           * View/Edit Schedule

                           * Track Medicines

                              * Used clickable text fields instead of icons for actions like “Add Medicine” to reduce reliance on symbolic interpretation

                              * Fixed button placement confusion:

                                 * “Done” in green to signal confirmation

                                 * “Add More” placed before “Done” to reflect sequence of execution and make use of KiH (Knowledge in the head).

                                    * Calendar navigation for month-wise tracking replicates familiar real-world metaphors

________________


Exercise & Therapy
                                       * Originally had a “Recommended” button, removed it to reduce clicks

                                       * Now shows recommended exercises up front

                                       * Categorized under:

                                          * Flexibility & Strength

                                          * Balance & Gait

                                          * Coordination

                                          * Breathing & Voice Therapy

                                             * Decided to keep categories for regular exercise usability, considering that they may want to do similar exercises to what was recommended to them on one day.

________________


Brain Games
To promote casual engagement while avoiding the stigma associated with mental health terminology, this section was renamed from Mental Health/Cognition to Brain Games, making the interactions of users more organic, especially for users in South Asia.
 Available Games:
                                                * Tile Matching

                                                * Sequence Matching

                                                * Whack-a-Mole

                                                * Spot the Difference


Flow and Navigation:
Back Icon: Will take you back to the previous page
Home Icon: Will take you directly to the home screen, from wherever you are in the app


Start Up Page:
Un-clickable:
                                                   * Settings : Will open your Android/IOS settings and take u to where you can turn on Accessibility settings


Clickable:
                                                   * Skip : close popup and show the main landing page
                                                   * Register: Take you to Create an Account
                                                   * Sign In: Take you to Sign In


Create an Account 
(Page 1):
Un-clickable:
                                                   * Full Name field
                                                   * DOB
                                                   * Date of Diagnosis
                                                   * Country
Clickable:
                                                   * Cancel : go back
                                                   * Next: next page of create account


(Page 2):
Un-clickable:
                                                   * Phone Number
                                                   * Password
                                                   * Checkboxes
                                                   * Read Here
                                                   * Unhide password
Clickable:
                                                   * Back : go back
                                                   * Next: Finish 
                                                   * (Will show you error messages the first time you click it)
                                                   * Clicking Next again will take you the main Home screen (after showing a loading screen)






Sign In:
Un-clickable:
                                                   * Phone Number
                                                   * Password
                                                   * CheckBox 
                                                   * Forgot Password
                                                   * Unhide password
Clickable:
                                                   * Sign In
                                                   *  will take you the main Home screen (after showing a loading screen)




Home Screen:
Un-clickable:
                                                   * None
Clickable:
                                                   * Settings icon (top-left) will take you to the Settings screen
                                                   * Profile icon (top-right) will take you to the Profile Screen


The buttons for the main features of the app are arranged in a 2x2 grid. 
Meaningful icons have been included in the buttons to help users understand what each feature does
                                                   * Track Your Symptoms
                                                   * Medication Manager
                                                   * Exercise & Therapy
                                                   * Brain Games
Will take you to the main screen for each feature
The ‘Upcoming Reminders’ screen is not clickable, it is only supposed to show the nearest upcoming medication reminder.


Profile: 
View your account details.
Un-clickable:
                                                   * None
Clickable:
                                                   * Edit : will take you to the Edit Profile screen, where you can edit all account details




Edit Profile: 
Un-clickable:
                                                   * All editable fields
Clickable
                                                   * Cancel will take you back to view Profile, discarding changes
                                                   * Save is supposed to update your Profile details.
In the Prototype, both do the same thing


Settings:
Un-clickable: 
                                                   * All except sign out
Only the ‘Sign Out’ button is clickable, pressing it will show a pop-up
                                                   * Pressing Cancel on the pop-up will return you to the settings screen
                                                   * Sign Out will take you to the landing page, where you can choose to register or login


Track Your Symptoms
Clickable:
                                                   * You can either click on Log Your Symptoms or Symptom History.
                                                   * If you click Log Your Symptoms, you can now either view or edit the symptoms for the specified day (today or yesterday) 
                                                   * If you click edit it shows you the No Symptoms Added screen, you can click on Add
                                                   * This takes you to the symptom logger where only the next, back and save buttons are clickable.
                                                   * If you had clicked the ‘view’ button it takes you to the view screen from where you can go back.
                                                   * If you had clicked Symptom History it takes you to the symtom history calendar where only the date 12 is clickable.
                                                   * Charts and download are also clickable.
                                                   * In download everything is clickable from there on






Medication Manager
Clickable:
                                                   1. Create Medicine Schedule: Will take you to add medicine
                                                   2. View/Edit Schedule: Will take you to Medicine Schedule
                                                   3. Track Medicines: Will take you to Track Medicines


                                                   1. Add Medicine:
Only follow this flow:
                                                   * Click the plus to increase the Frequency to 2
                                                   * Click Add More
                                                   * Click plus again
                                                   * Click on Done
        You will be taken to Medicine Schedule
        
        
                                                   2. View/Edit Schedule
You will start at Medicine Schedule, where you view your schedule
                                                   * CLick Edit : Will take you to edit Schedule
                                                   * Delete Centrum (You can cancel or delete)
                                                   * Once you have deleted Centrum
                                                   * Edit Levadopa
                                                   * Just click Done (other fields are not interactable)
                                                   * Done will take you back
                                                   * Click on Add Medicine
                                                   * Click on Done


        
                                                   3. Track Medicines
                - Download button will show a popup, click yes to download or no to cancel




Exercise & Therapy:
In the recommended videos on Tandem Walking is clickable
All the category buttons are clickable, and will take you to the appropriate screen


Therapy Category Screens:
Display videos for each category.
                                                   * Flexibility & Strength
                                                   * Balance & Gait  (contains a clickable video)
                                                   * Coordination
                                                   * Breathing & Voice Therapy


Only ‘Tandem Walking’ which comes under Balance & Gait is clickable, clicking it will take you to the in-app video player.


In-app video player:
                                                   * Pause icon (not interactable)
                                                   * Full screen icon (takes you to full screen mode)
Full screen player: 
                                                   * Normal Screen icon takes you back to the previous screen
                                                   * Minimize icon does the same




Brain Games:
When a user selects a game from the Brain Games main screen:
                                                   1. They are first taken to an Instructions Screen, which outlines how to play.

                                                   2. After reading the instructions, the user taps the "Play" button.

                                                   3. This navigates to a Game Screen, which visually simulates what gameplay would look like.
                                                   4. The back button takes the user to the main brain games page

                                                      * These game screens are mock-ups only. The actual games are not playable in this prototype
                                                      * Only the UI and feedback visuals (score, high score, layout) have been designed.

Back button takes the user directly back to the main Brain Games screen.