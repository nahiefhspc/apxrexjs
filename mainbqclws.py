import requests
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Your Telegram bot token
TOKEN = "8105693058:AAHxEz9Fo6xSLS9cHPa-6p_imje4HHufgd0"

# Headers for API request
HEADERS = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website",
    "User-Agent": "",
    "Referer": "https://voraclasses.com/"
}

# Data lists
FIRST_NAMES = [
    "Aarav", "Aarya", "Aayush", "Abhay", "Abhinav", "Aditya", "Advait", "Ahaan", "Akhil", "Amar",
    "Aniket", "Anirudh", "Ansh", "Arjun", "Aryan", "Ashwin", "Atharv", "Bhavesh", "Chirag", "Daksh",
    "Darshan", "Dev", "Devansh", "Dhruv", "Divyansh", "Eshaan", "Gautam", "Girish", "Hardik", "Harsh",
    "Himanshu", "Ishaan", "Jatin", "Jeevan", "Kabir", "Karan", "Krish", "Lakshay", "Lalit", "Madhav",
    "Mayank", "Mohit", "Nakul", "Nihal", "Nikhil", "Ojas", "Om", "Parth", "Pranav", "Pratham",
    "Raj", "Rajesh", "Ravi", "Reyansh", "Rishi", "Rohit", "Rudra", "Samar", "Samarth", "Sandeep",
    "Sanjay", "Sarthak", "Shaurya", "Shivansh", "Shrey", "Siddharth", "Soham", "Subham", "Surya", "Tanish",
    "Tarun", "Uday", "Varun", "Vikram", "Vishal", "Vivaan", "Yash", "Zaid", "Aditi", "Aisha",
    "Akanksha", "Amrita", "Ananya", "Anika", "Anjali", "Ankita", "Aradhya", "Avni", "Bhavya", "Charvi",
    "Chhavi", "Damini", "Deepika", "Divya", "Ekta", "Esha", "Falguni", "Gauri", "Gayatri", "Harini",
    "Ishita", "Janhvi", "Jaya", "Juhi", "Kajal", "Kavya", "Khushi", "Kirti", "Lakshmi", "Lavanya",
    "Madhavi", "Mahima", "Maitreyi", "Meera", "Mira", "Mitali", "Nandini", "Navya", "Neha", "Nidhi",
    "Nikita", "Nisha", "Nithya", "Ojaswini", "Pallavi", "Pari", "Payal", "Pooja", "Prachi", "Pragya",
    "Pranavi", "Preeti", "Priya", "Rachna", "Radha", "Rashi", "Ria", "Richa", "Ritika", "Riya",
    "Saanvi", "Sakshi", "Samiksha", "Sanjana", "Sharvani", "Sharvya", "Shivani", "Shravani", "Shruti", "Simran",
    "Sita", "Sneha", "Sonal", "Sonali", "Suhani", "Sunita", "Swara", "Tanisha", "Tanya", "Trisha",
    "Udita", "Vaishnavi", "Vani", "Vanya", "Varsha", "Vasudha", "Vibha", "Vidhi", "Vidya", "Yamini",
    "Yashasvi", "Zoya", "Abhilash", "Ajay", "Alok", "Amit", "Anand", "Arpit", "Ashish", "Balaji",
    "Bharat", "Bhupesh", "Chaitanya", "Chetan", "Dhananjay", "Dheeraj", "Dilip", "Dinesh", "Eklavya", "Gagan",
    "Gopal", "Harish", "Harsha", "Hemant", "Hitesh", "Indrajit", "Jagannath", "Jayesh", "Kailash", "Keshav",
    "Kiran", "Krishna", "Laxman", "Mahesh", "Manish", "Manoj", "Mohan", "Mukesh", "Naveen", "Navin",
    "Neeraj", "Omkar", "Pankaj", "Prakash", "Pratap", "Raghav", "Ramesh", "Ranveer", "Rupesh", "Sagar",
    "Sanjeev", "Sarvesh", "Satish", "Shankar", "Shantanu", "Sharad", "Suresh", "Swapnil", "Tejas", "Tushar",
    "Umesh", "Uttam", "Venkatesh", "Vignesh", "Vinay", "Vinod", "Vishnu", "Yogesh", "Abha", "Ahana",
    "Alisha", "Anusha", "Arpita", "Ashmita", "Bharti", "Bhumika", "Chanda", "Chitra", "Deepti", "Dhanya",
    "Disha", "Geeta", "Gomathi", "Harsha", "Indira", "Ira", "Ishwari", "Jaya", "Kalyani", "Kamini",
    "Kusum", "Lata", "Madhuri", "Manjari", "Meenal", "Minakshi", "Mridula", "Nalini", "Namita", "Nayana",
    "Neetu", "Nirmala", "Padma", "Pranjali", "Pushpa", "Ranjana", "Rekha", "Renuka", "Rohini", "Rupali",
    "Sadhana", "Sarita", "Seema", "Shailee", "Sheetal", "Shraddha", "Smita", "Sudha", "Supriya", "Sushma",
    "Swati", "Tanuja", "Urmila", "Vibha", "Yogita", "Anupam", "Ashutosh", "Avadhesh", "Chiranjiv", "Deepesh",
    "Devendra", "Dharam", "Gajendra", "Gulshan", "Himadri", "Irfan", "Jitendra", "Kamal", "Karanveer", "Madan",
    "Mithun", "Narayan", "Nishant", "Prafull", "Ravindra", "Satyendra", "Shubham", "Siddhanth", "Somnath", "Tanveer",
    "Vidyut", "Yudhishthir"
]
SURNAMES = [
    "Agarwal", "Ahluwalia", "Ahuja", "Amin", "Anand", "Apte", "Arora", "Arya", "Ashraf", "Asthana",
    "Bajpai", "Bakhshi", "Balakrishnan", "Balasubramanian", "Banerjee", "Bansal", "Barua", "Basu", "Bedi", "Bhagat",
    "Bhalla", "Bhandari", "Bharadwaj", "Bhargava", "Bhattacharya", "Bhuyan", "Biswas", "Bose", "Chakraborty", "Chand",
    "Chandra", "Chaturvedi", "Chauhan", "Chawla", "Cherian", "Chhibber", "Chopra", "Choudhary", "Chowdhury", "Dalal",
    "Dandekar", "Das", "Dasgupta", "Datta", "Dave", "Dayal", "Desai", "Deshmukh", "Dev", "Dey",
    "Dhaliwal", "Dhar", "Dhawan", "Dixit", "Dubey", "Duggal", "Dutta", "Gadre", "Gahlot", "Gandhi",
    "Ganguly", "Garg", "Ghosh", "Goel", "Gokhale", "Gopal", "Goswami", "Goyal", "Guha", "Gupta",
    "Haldar", "Handa", "Hegde", "Hora", "Iyer", "Jain", "Jaiswal", "Jani", "Jaswal", "Jha",
    "Jhunjhunwala", "Joshi", "Kaimal", "Kakkar", "Kalita", "Kamat", "Kamdar", "Kapadia", "Kapoor", "Karan",
    "Kashyap", "Kathuria", "Kaul", "Kaushik", "Kejriwal", "Kelkar", "Khan", "Khanna", "Khatri", "Khurana",
    "Kini", "Kohli", "Kolhe", "Kothari", "Kulkarni", "Kumar", "Lakhani", "Lal", "Lamba", "Lohani",
    "Lohia", "Madan", "Mahajan", "Maheshwari", "Mahindra", "Malhotra", "Malik", "Mani", "Manjrekar", "Mansingh",
    "Marathe", "Mathur", "Matur", "Mazumdar", "Mehra", "Menon", "Mehta", "Mishra", "Modi", "Mohanty",
    "Mookerjee", "Mukherjee", "Muni", "Munshi", "Murthy", "Nadkarni", "Nair", "Nambiar", "Nanda", "Narang",
    "Narayan", "Narayanan", "Nath", "Naidu", "Nayak", "Nayar", "Nigam", "Ojha", "Pandey", "Pandit",
    "Panikar", "Panjwani", "Parekh", "Parikh", "Patel", "Pathak", "Patil", "Pattanaik", "Pawar", "Pillai",
    "Pradhan", "Prakash", "Purohit", "Raghavan", "Rai", "Rajan", "Rajput", "Ram", "Ramakrishnan", "Raman",
    "Ramaswamy", "Rana", "Ranganathan", "Rao", "Rastogi", "Rath", "Rathore", "Raval", "Ray", "Reddy",
    "Roy", "Sagar", "Sahni", "Saini", "Saksena", "Samal", "Sampath", "Sanghvi", "Saran", "Sarin",
    "Saroj", "Sastry", "Sathe", "Saxena", "Sen", "Sengupta", "Setia", "Setty", "Shah", "Shaikh",
    "Shanbhag", "Shankar", "Sharma", "Shetty", "Shinde", "Sibal", "Sikri", "Sinha", "Sircar", "Somani",
    "Srivastava", "Subramanian", "Sundaram", "Swamy", "Talwar", "Tandon", "Taneja", "Tewari", "Thakur", "Thakkar",
    "Thapar", "Tilak", "Trivedi", "Tyagi", "Upadhyay", "Varma", "Venkatesan", "Verma", "Vora", "Wadhwa",
    "Wagle", "Yadav", "Acharya", "Acharjee", "Adhikari", "Aggarwal", "Amin", "Bagchi", "Baig", "Bajaj",
    "Bakshi", "Bal", "Banthia", "Bari", "Barve", "Basu", "Bhandarkar", "Bhonsle", "Bhutani", "Bijlani",
    "Bisoi", "Chaudhary", "Chaudhuri", "Chawre", "Chogle", "Chopde", "Chugh", "Dabral", "Daga", "Damle",
    "Dandavate", "Daruwala", "Datir", "Deshpande", "Dhamdhere", "Dhande", "Dhandapani", "Dharwadkar", "Dhoke", "Dhuri",
    "Duggal", "Ekbote", "Fadnavis", "Ganatra", "Garge", "Gogate", "Gokul", "Gund", "Hajela", "Harikrishnan",
    "Hiremath", "Ilaiah", "Iyengar", "Jaitley", "Jha", "Joglekar", "Kadu", "Kalaskar", "Kamble", "Kanjirath",
    "Kapur", "Karkare", "Karnik", "Karunakar", "Kasturi", "Kattimani", "Kavadi", "Khare", "Khot", "Kinnari",
    "Kolekar", "Konde", "Kothare", "Krishnan", "Kulshreshtha", "Lad", "Laxman", "Lokhande", "Loni", "Mahale",
    "Mahidhar", "Makhija", "Mali", "Mallick", "Manchanda", "Manian", "Mannadi", "Marathe", "Mekapati", "Modak",
    "Mukadam", "Murugesan", "Nadkarni", "Nanda", "Nayyar", "Padgaonkar", "Pallavi", "Pangarkar", "Parab", "Paranjape",
    "Pendharkar", "Peshwe", "Phadnis", "Pillay", "Ponmudi", "Rajagopalan", "Rajendran", "Ramaswami", "Ranaut", "Ranawat",
    "Rangnekar", "Raut", "Rawat", "Raychowdhury", "Samdani", "Sawhney", "Sehgal", "Shailendra", "Shanbhogue", "Tamhane",
    "Tandon", "Tendulkar", "Thirumalai", "Tiwary", "Tripathi", "Udani", "Upreti", "Vaidya", "Vishwakarma", "Zutshi"
]
LINKS = [
    "ebooks/jee-main-preparation-tips-complete-strategy-study-plan",
    "ebooks/jee-main-highest-scoring-chapters-and-topics",
    "sample-papers/jee-main-10-full-mock-test-and-explanations-pdf",
     "ebooks/jee-main-previous-10-year-questions-detailed-solutions",
      "sample-papers/bitsat-sample-paper",
]
LOCATIONS = [
    "Mumbai, Maharashtra, India",
    "Bangalore, Karnataka, India",
    "Chennai, Tamil Nadu, India",
    "Kolkata, West Bengal, India",
    "Hyderabad, Telangana, India",
    "Ahmedabad, Gujarat, India",
    "Pune, Maharashtra, India",
    "Lucknow, Uttar Pradesh, India",
    "Chandigarh, Punjab, India",
    "Bhopal, Madhya Pradesh, India"
]

async def check_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Checks numbers in a given range and sends updates."""
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /check <start_range> <end_range>")
        return

    try:
        start_range = int(context.args[0])
        end_range = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Please enter valid numbers.")
        return

    await update.message.reply_text(f"Checking numbers from {start_range} to {end_range}...")

    found_numbers = []
    progress_message = await update.message.reply_text("Progress: 0 numbers checked.")

    for i, number in enumerate(range(start_range, end_range + 1), 1):
        url = f"https://voraclassesapi.classx.co.in/get/check_user_exist?email_or_phone={number}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            try:
                data = response.json()
                if "User exist" in str(data):  # Adjust based on actual response
                    this_link = random.choice(LINKS)
                    first_name = random.choice(FIRST_NAMES)
                    surname = random.choice(SURNAMES)
                    random_digits = random.randint(10, 99)
                    email = f"{first_name}{surname}{random_digits}@gmail.com"
                    location = random.choice(LOCATIONS)

                    # ✅ Format the message in HTML
                    found_text = f"""
<pre>
{this_link} - {number} - {first_name} {surname} - {email} - {location}
</pre>
"""
                    found_numbers.append(found_text)
                    await update.message.reply_text(found_text, parse_mode="HTML")

            except Exception as e:
                print(f"Error parsing response for {number}: {e}")

        # Update progress every 1000 numbers
        if i % 1000 == 0:
            await progress_message.edit_text(f"Progress: {i} numbers checked. Last checked: {number}")

    await progress_message.edit_text(f"✅ Finished checking! Total numbers checked: {end_range - start_range + 1}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await update.message.reply_text("Send `/check <start_range> <end_range>` to check numbers.", parse_mode="MarkdownV2")

# Initialize the bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start, block=False))
    app.add_handler(CommandHandler("check", check_numbers, block=False))

    print("🤖 Bot is running...")
    app.run_polling()

# Run for Pydroid 3
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
