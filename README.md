# Auto Tint 

Using Ren'Py 7.4 matrixcolor to provide a smooth (over duration) tint of displayables.

This is a pretty basic piece of code which allows for separating the tint (or tints) from the images using them as well as providing a smooth dissolve like transition from one tint to the next.

It is mostly aimed at situations where a developer wants to subtely tint their sprites and/or backgrounds to show changes in the time of day. For example:

```py
default day_period_tint = TintData()

label badger_house_evening:

    scene bg badgerhouse at autotint(day_period_tint)

    show badger at autotint(day_period_tint):
        align (0.5, 1.0)

    badger "Looks like evening is setting in"

    $ day_period_tint.set("#43A")

    badger "Yup, definitely evening as everything has gone rather blue"

    badger "It's almost too dark to find the light switch. Eek"
```
    
The notes in the rpy file should pretty much cover how the system is used.

#### Caveats:

If you just want various layers tinted (hair, skin, clothes etc) you would likely do better just using a matrixcolor TintMatrix directly rather than this fading in one.

Smooth fading during rollback and rollforward is disabled in favour of just instant tinting (which works better in those areas)
