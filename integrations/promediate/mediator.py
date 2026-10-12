"""Experimental ProMediate plugin. Requires upstream dependencies and a transport.
Not a claim of end-to-end compatibility: see README and readiness report.
"""
from thoughtful_agents.models.participant import Mediator
from .bridge import messages, parse_decision

class ProtocolMediator(Mediator):
    def __init__(self, *args, completion, condition='protocol', **kwargs):
        super().__init__(*args, **kwargs)
        self.completion = completion
        self.condition = condition
        self.audit = []

    async def act(self, conversation, event):
        self.next_utterance = None
        if event.participant_id == self.id:
            return []
        self.next_utterance = await self.decide_when_and_how(conversation)

    async def decide_when_and_how(self, conversation):
        context, history, memories, thoughts = self.prepare(conversation)
        request = messages(self.condition, {'context':context,'history':history,
                                           'mediator_memories':memories})
        # Transport owns model/settings, usage logging, timeout and call limits.
        # Parsing errors propagate: never count them as a successful quiet turn.
        raw = await self.completion(request, model=self.model)
        decision = parse_decision(raw)
        self.audit.append({'request':request,'response':raw})
        return decision['utterance'] if decision['intervene'] else None

    def decide_when(self, *args):
        raise NotImplementedError('Use combined mode')

    async def decide_how(self, *args):
        raise NotImplementedError('Use combined mode')
