
# class GestureClassifier:

#     def classify(self, tracked_hands):

#         classified_hands = []

#         for hand in tracked_hands:

#             fingers = hand["fingers"]

#             thumb = fingers["thumb"]
#             index = fingers["index"]
#             middle = fingers["middle"]
#             ring = fingers["ring"]
#             pinky = fingers["pinky"]

#             gesture = "Unknown"

#             # Rock: All fingers folded
#             if not any(fingers.values()):
#                 gesture = "Rock"

#             # Paper: All fingers extended
#             elif all(fingers.values()):
#                 gesture = "Paper"

#             # Scissors: Only index and middle fingers extended
#             elif (
#                 not thumb
#                 and index
#                 and middle
#                 and not ring
#                 and not pinky
#             ):
#                 gesture = "Scissors"

#             classified_hands.append({
#                 "hand_index": hand["hand_index"],
#                 "handedness": hand["handedness"],
#                 "gesture": gesture
#             })

#         return classified_hands



class GestureClassifier:

    def classify(self, tracked_hands):

        classified_hands = []

        for hand in tracked_hands:

            fingers = hand["fingers"]

            index = fingers["index"]
            middle = fingers["middle"]
            ring = fingers["ring"]
            pinky = fingers["pinky"]
            thumb = fingers["thumb"]

            gesture = "Unknown"

            # Rock: Four main fingers are folded
            if not index and not middle and not ring and not pinky:
                gesture = "Rock"

            # Paper: All five fingers are extended
            elif all(fingers.values()):
                gesture = "Paper"

            # Scissors: Index and middle fingers extended
            elif (
                index
                and middle
                and not ring
                and not pinky
            ):
                gesture = "Scissors"

            classified_hands.append({
                "hand_index": hand["hand_index"],
                "handedness": hand["handedness"],
                "gesture": gesture
            })

        return classified_hands
