from botbuilder.core import TurnContext
from botbuilder.schema import ChannelAccount
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo

class MyBot(TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        teams_members = await TeamsInfo.get_members(turn_context)
        for teams_member in teams_members:
            if teams_member.id == turn_context.activity.from_property.id:
                user_email = teams_member.email if teams_member.email else None
                if user_email:
                    await turn_context.send_activity(f"You said '{ turn_context.activity.text }' and your email is {user_email}")
                else:
                    await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello!")
