from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

# A list to store the rides
rides = []

# Define keyboard layout
reply_keyboard = [
    ['Create a Ride'],
    ['Book a Ride'],
    ['See List of Rides']
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

# Define constants for state management
CREATE_TRIP, BOOK_TRIP, VIEW_TRIPS, ASK_FROM, ASK_TO, SELECT_RIDE = range(6)

async def start(update: Update, context):
    await update.message.reply_text(
        "Welcome! Please choose an option:",
        reply_markup=markup
    )
    return CREATE_TRIP


async def create_trip(update: Update, context):
    await update.message.reply_text("Where are you starting from?")
    return ASK_FROM


async def ask_from(update: Update, context):
    context.user_data['from'] = update.message.text
    await update.message.reply_text("Where are you going to?")
    return ASK_TO


async def ask_to(update: Update, context):
    context.user_data['to'] = update.message.text
    from_location = context.user_data['from']
    to_location = context.user_data['to']

    # Store the ride details
    ride = {'from': from_location, 'to': to_location, 'user': update.effective_user.username}
    rides.append(ride)

    # Confirmation message
    await update.message.reply_text(f"Trip created from {from_location} to {to_location}.")
    return ConversationHandler.END


async def view_trips(update: Update, context):
    if not rides:
        await update.message.reply_text("No rides available at the moment.")
    else:
        ride_list = "\n".join([f"From: {ride['from']}, To: {ride['to']}, By: {ride['user']}" for ride in rides])
        await update.message.reply_text(f"Available rides:\n{ride_list}")
    return ConversationHandler.END


async def book_trip(update: Update, context):
    if not rides:
        await update.message.reply_text("No rides available to book.")
        return ConversationHandler.END
    else:
        # Show available rides with indices
        ride_list = "\n".join([f"{idx+1}. From: {ride['from']}, To: {ride['to']}, By: {ride['user']}" for idx, ride in enumerate(rides)])
        await update.message.reply_text(f"Available rides:\n{ride_list}\n\nPlease select a ride by number:")
        return SELECT_RIDE


async def select_ride(update: Update, context):
    try:
        selected_ride_idx = int(update.message.text) - 1  # Convert input to index
        if 0 <= selected_ride_idx < len(rides):
            booked_ride = rides.pop(selected_ride_idx)  # Remove the selected ride
            await update.message.reply_text(f"You have successfully booked the ride from {booked_ride['from']} to {booked_ride['to']} by {booked_ride['user']}.")
        else:
            await update.message.reply_text("Invalid selection. Please try again.")
            return SELECT_RIDE
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return SELECT_RIDE

    return ConversationHandler.END
