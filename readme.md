#################################################
#                                               #
#       name: interpreter                       #
#       author: David Möller                    #
#                                               #
#                                               #
#                                               #
#                                               #
#################################################

Description: This module accepts a string, which is
             analysed and interpreted using
             keywords to extract organize
             and return useful information.


Funktion:    After deciding, if the input string is
             a request of the patient or documentation
             of the nurse or doctor these cases are
             handeled seperately.
             Requests are sorted by priority looking
             for words signaling urgency and send
             to the nurse station.
             Documentation is organized in a library
             using keywords and their synonyms and
             made available for further use.
