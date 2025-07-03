# Assignment2_4080
How to run the program.
1.Make sure you have python installed on your computer
2.Open terminal/cmd in the same folder as the py script
3. Run the script with python ai_assistant.py
4. Follow the prompts on the console

Overview of the assistant functionality
The script first will collect basic user details like their name and age to store them into userProfile.
Then the user will pick one of the three of Music, Fitness, or Study Assistant to specify the type of help the AI needs to give.
Each input given by the user is wrapped in a request object which is then fed into the handleRequest method to that helps route into its specific generateResponse logic to give the response of the recommendation, the confidence score, and a flag to determine whether an action was performed

Which concepts were implemented where:
Primite Types: userProfile, Request, and Response use str, int, bool, and float
Complex Types: preferences:Dict[strr, Any] in UserProfile
Enum: CommandType enum defines three command categories
Validation: __post__init in each data-class to check for correct types
Encapsulation: recommendPlayist and suggestWorkout
Plymorphism/Inheritence: AIAssistannt abstract base class defines greetUser, handleRequest, and abstracty generateResponse. Also each subclass overrides generateResponse