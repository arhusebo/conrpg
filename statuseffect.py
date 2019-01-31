class StatusEffect:
    def __init__(self, actor, duration):
        self.actor = actor
        self.duration = duration
        self.active = True

    def tick(self):
        if self.duration <= 0:
            self.active = False
        if self.active:
            self.action()
            self.duration -= 1

    def action(self):
        pass

class HealingEffect(StatusEffect):
    def __init__(self, value, *args):
        super().__init__(self, *args)
        self.value = value

    @Override
    def action(self):
        self.actor.stats.health += value

class AttackEffect(StatusEffect):
    def __init__(self, value, *args):
        self.value = value
        super().__init(self, *args)

    @Override
    def action(self):
        self.actor.effect_stats.attack += value
