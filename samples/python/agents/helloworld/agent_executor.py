from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


# --8<-- [start:HelloWorldAgentExecutor_init]
class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    # --8<-- [end:HelloWorldAgentExecutor_init]
    # --8<-- [start:HelloWorldAgentExecutor_execute]
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Echo back the received text
        query = context.get_user_input()

        if query:
            # Echo back the received text
            await event_queue.enqueue_event(new_agent_text_message(query))
        else:
            # Handle cases where the message might be empty or malformed
            await event_queue.enqueue_event(
                new_agent_text_message('No message content found.')
            )

    # --8<-- [end:HelloWorldAgentExecutor_execute]

    # --8<-- [start:HelloWorldAgentExecutor_cancel]
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

    # --8<-- [end:HelloWorldAgentExecutor_cancel]
