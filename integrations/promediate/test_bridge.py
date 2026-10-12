import asyncio
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from .bridge import ROOT, messages, parse_decision, replay_context

class Checks(unittest.TestCase):
    def test_cases_do_not_leak_rubric_or_future_turn(self):
        cases=json.loads((ROOT/'evaluations/workplace/cases.json').read_text())['cases']
        self.assertEqual(len({c['id'] for c in cases}),6)
        for c in cases:
            first=json.dumps(messages('basic',replay_context(c,0)))
            self.assertNotIn(c['turns'][1]['content'],first)
            self.assertNotIn('review_only',first)
            self.assertNotIn('expected_by_turn',first)
            second=replay_context(c,1,'actual response')
            self.assertEqual(second['history'][1]['content'],'actual response')
    def test_strict_decision(self):
        self.assertFalse(parse_decision('{"intervene":false,"utterance":""}')['intervene'])
        for bad in ['{}','[]','{"intervene":"false","utterance":""}',
                    '{"intervene":false,"utterance":"Speak"}',
                    '{"intervene":true,"utterance":""}']:
            with self.assertRaises(ValueError): parse_decision(bad)
    def test_condition_and_prior_required(self):
        with self.assertRaises(ValueError): messages('social',{})
        with self.assertRaises(ValueError): replay_context({'turns':[{}]},1)
    def test_plugin_wiring_with_stub_base(self):
        # Tests our logic only. Does not import or validate upstream dependencies.
        stub=types.ModuleType('thoughtful_agents.models.participant')
        class Base:
            def __init__(self, **kw): self.id='mediator'; self.model='fixed-model'
            def prepare(self,c): return 'context','history','public memory','unused'
        stub.Mediator=Base
        name='thoughtful_agents.models.participant'
        old=sys.modules.get(name)
        sys.modules[name]=stub
        try:
            from .mediator import ProtocolMediator
            replies=iter(['{"intervene":true,"utterance":"A question"}',
                          '{"intervene":false,"utterance":""}'])
            async def complete(request,model):
                self.assertEqual(model,'fixed-model')
                return next(replies)
            p=ProtocolMediator(completion=complete)
            event=types.SimpleNamespace(participant_id='person')
            asyncio.run(p.act(None,event)); self.assertEqual(p.next_utterance,'A question')
            asyncio.run(p.act(None,event)); self.assertIsNone(p.next_utterance)
            self.assertEqual(len(p.audit),2)
        finally:
            if old is None: sys.modules.pop(name,None)
            else: sys.modules[name]=old

if __name__=='__main__': unittest.main()
