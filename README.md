![help-activity-icon](images/Activity-help.svg)

Help is an activity which aims to provide users with easy access to documentation and manuals

Help can be accesed
* as a [standalone activity](http://activities.sugarlabs.org/en-US/sugar/addon/4051)
* from [within another activity](#help-from-within-another-activity)
* at https://help.sugarlabs.org/

### How to edit Help and Contribute:
[Read here](source/how_to_help.rst)

### Help from within another activity:

When contextual help( <kbd>alt</kbd> + <kbd>shift</kbd> + <kbd>h</kbd> ) is requested from within an sugar activity, the [helplink.json](helplink.json) file matches the bundle_id(the same as defined in the particular activity.info file) with a corresponding html page and renders its content in a tiny browser.

### How to translate:
https://github.com/godiard/help-activity/blob/master/howto_translate.rst

###### More information at
http://wiki.sugarlabs.org/go/Activities/Help/Contribute

Contact: godiard@gmail.com
