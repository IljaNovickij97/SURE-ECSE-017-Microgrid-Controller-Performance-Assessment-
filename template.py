# This template is for metric evaluation
# No need to import matplotlib, it's done in gui.py
# All calculations done here so numpy will probably be imported here
# Add more arguements to __init__ to do fancy stuff like decide what kind of calculations to do etc.

class TemplateMetric(object):
    def __init__(self):
        # Put stuff here if using variables throughout the class i.e. something that's calculated for all of the methods
        # below

    @staticmethod
    def template_calculation_plot(data, canvas):
        # Do calculations here
        #canvas.axes.plot(x,y)