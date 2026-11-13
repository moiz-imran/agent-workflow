Document operations return notification recipients for moves and saves.
A move updates the folder in place, keeps followers and sends no notifications.
A copy returns an independent document in the destination with no followers;
it leaves every original field untouched. Body and folder are strings; followers
are a list of strings. A save stores the new body, notifying followers only when
whitespace-separated words differ. Whitespace-only changes never notify.
