import random

from transitions import Machine


class NarcolepticSuperheroModel:


    def __init__(self, name):
        self.name = name

        self.kittens_rescued = 0

    def update_journal(self):
        self.kittens_rescued += 1

    @property
    def is_exhausted(self):
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")


        # state machine
class NarcolepticSuperheroMachine(Machine):
    states = ['asleep', 'hanging out', 'hungry', 'sweaty', 'saving the world']

    def __init__(self, model):
        super().__init__(model=model, states=NarcolepticSuperheroMachine.states, initial='asleep')

        self.add_transition(trigger='wake_up', source='asleep', dest='hanging out')
        self.add_transition(trigger='work_out', source='hanging out', dest='hungry')
        self.add_transition(trigger='eat', source='hungry', dest='hanging out')

        self.add_transition(trigger='distress_call', source='*', dest='saving the world',
                                    before='change_into_super_secret_costume')

        self.add_transition(trigger='complete_mission', source='saving the world', dest='sweaty',
                                    after='update_journal')

        self.add_transition(trigger='clean_up', source='sweaty', dest='asleep', conditions=['is_exhausted'])
        self.add_transition(trigger='clean_up', source='sweaty', dest='hanging out')

        self.add_transition(trigger='nap', source='*', dest='asleep')

def main():
    batman_model = NarcolepticSuperheroModel("Batman")
    batman = NarcolepticSuperheroMachine(batman_model)
    print(batman.model.state)

    batman.model.wake_up()
    print(batman.model.state)

    batman.model.nap()
    print(batman.model.state)

    # batman.clean_up()
    # => MachineError: "Can't trigger event clean_up from state asleep!"

    batman.model.wake_up()
    batman.model.work_out()
    print(batman.model.state)

    print(batman.model.kittens_rescued)

    batman.model.distress_call()
    print(batman.model.state)

    batman.model.complete_mission()
    print(batman.model.state)

    print(batman.model.kittens_rescued)

    batman.model.clean_up()
    print(batman.model.state)

if __name__ == '__main__':
    main()
