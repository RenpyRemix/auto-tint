## To view example in your game add
##
##  call autotint_example
##
## somewhere in your running label script



            ###########################################
            #                                         #
            #           To use in your game           #
            #                                         #
            #   Make sure the Python stuff and the    #
            #   transform are available (basically,   #
            #   just do not delete them)              #
            #   Then just do similar to the example   #
            #   usage below                           #
            #                                         #
            ###########################################

# You may need to allow gl2 to operate by setting the config
define config.gl2 = True

# Set up a variable to store the desired tint (default is #FFF no tint)
default day_period_tint = TintData()

# Just a test image to view it working
image testtint = Composite(
    (100, 180),
    *[f for g in [
        [(0, h*5), 
         Solid(Color("#BBB").interpolate(Color("#555"), h/36.0), xysize=(100, 10))]
         for h in range(36)] 
     for f in g])

label autotint_example:

    scene expression "#888"

    # show the image at the transform and pass in the TintData object
    show testtint at autotint(day_period_tint):
        align (0.5, 0.5)

    "Before tint to green"

    # Changing the tint is done by using set() on the TintData object
    # Any images using the transform with that object will re-tint to match
    $ day_period_tint.set("#3E4")

    "After tint to green"

    "Before tint to blue (over 3 seconds)"

    # You can also change the duration easily
    $ day_period_tint.set("#43E", 3)

    "After tint to blue"

    "Before tint to red (over 4.5 seconds)"

    $ day_period_tint.set("#E34", 4.5)

    "After tint to red"

    return



            ###########################################
            #                                         #
            #     The Python stuff and transform      #
            #                                         #
            #    Keep this as it is, even if you      #
            #    delete the example stuff above       #
            #                                         #
            ###########################################

init python:

    import time

    class TintData(object):

        def __init__(self, tint=None):
            self.current_tint = Color("#FFF")
            self.start_tint = None
            self.end_tint = None
            self.start_time = -1.0
            self.duration = 1.0
            self.set(tint)

        def set(self, tint=None, duration=None):

            tint = Color(tint or "#FFF")

            self.start_tint = self.current_tint

            self.end_tint = tint

            if duration is not None:
                self.duration = duration

            self.start_time = -1.0

        def __repr__(self):
            return "TintData: {}".format(self.__dict__)


    def tint_function(trans, st, at, tint_obj=None):

        if not isinstance(tint_obj, TintData):
            raise "Transform autotint must be provided a TintData object"

        if tint_obj.start_time < 0.0:
            tint_obj.start_time = time.time()

        if tint_obj.current_tint != tint_obj.end_tint:
            used_at = (time.time() - tint_obj.start_time) / tint_obj.duration
            used_at = min(1.0, max(0.0, used_at))

            tint_obj.current_tint = tint_obj.start_tint.interpolate(
                    tint_obj.end_tint, 
                    used_at)

            if used_at == 1.0 or renpy.in_rollback():

                tint_obj.current_tint = tint_obj.end_tint
                tint_obj.start_tint = tint_obj.end_tint

        trans.matrixcolor = TintMatrix(tint_obj.current_tint) 

        return 0.1 if tint_obj.current_tint == tint_obj.end_tint else 0.0


transform autotint(tint_obj=day_period_tint):
    mesh True
    function renpy.curry(tint_function)(tint_obj=tint_obj)
