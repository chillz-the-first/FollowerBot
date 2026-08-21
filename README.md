# InstaFollower Bot

A Selenium bot that follows everyone who follows a target account, in the hope some of them follow back. Built for Day 52 of the *100 Days of Code* course, targeting Share-a-Naan (an Instagram clone) rather than the real Instagram to avoid bot detection.

## What it does

1. Logs into Share-a-Naan and dismisses the "save login" and "notifications" popups.
2. Opens a target account's followers list and scrolls it until every follower has loaded.
3. Clicks Follow on each one, skipping accounts you already follow.

## Tech stack

- Python 3.13
- Selenium
- python-dotenv (for credentials and config)
- Chrome + ChromeDriver

## Setup

Clone the repo and install the dependencies:

```bash
 pip install selenium python-dotenv
```

Create a `.env` file in the project root:

```
IG_USERNAME=your-username
PASSWORD=your-password
SIMILAR_ACCOUNT=target-account-handle
BASE_URL=your-share-a-naan-base-url
LOGIN_URL=your-share-a-naan-login-url
```

`SIMILAR_ACCOUNT` is the account whose followers you want to follow. `IG_USERNAME` is namespaced on purpose so it can't collide with the `USERNAME` environment variable some operating systems set by default.

## Run

```bash
 python main.py
```

Chrome opens, logs in, loads the target's follower list, and follows each account you're not already following. It prints a running count of how many new accounts it followed.

## Design notes

**Adaptive scrolling.** The followers list loads more names only as you scroll inside its dialog. Rather than scrolling a fixed number of times, the bot scrolls until the container's height stops growing, and confirms that twice in a row before stopping. This adapts to any list size instead of guessing, and the double-confirmation guards against stopping early on a slow network load.

**Stale element handling.** Clicking a follow button re-renders that row, which invalidates any stored reference to it. Instead of holding a list of button objects and clicking them, `follow()` re-finds each button fresh by index on every iteration, so a re-render from the previous click can't leave it holding a stale reference.

**Per-item error handling.** Each click is wrapped in a `try/except` for `StaleElementReferenceException` and `ElementClickInterceptedException`. One failed click is logged and skipped rather than ending the whole run.

**Skip already-followed accounts.** Before clicking, the bot checks whether a follow button already carries the `is-following` class and skips it. This avoids triggering the "Unfollow?" confirmation dialog that appears when you click an account you already follow.

**Explicit waits.** Every interaction uses `WebDriverWait` with `expected_conditions` rather than fixed `sleep()` calls, so each step waits exactly as long as the page needs. The one exception is the scroll loop, where a short fixed pause per scroll is the practical choice.

**Guarded cleanup.** `bot` is set to `None` before the `try` block, so the `finally` block's `if bot is not None` check can safely skip `driver.quit()` if the constructor itself failed.

## Notes

- ChromeDriver is managed automatically by Selenium Manager (bundled with recent Selenium versions).
- Add `.env` to your `.gitignore` so you don't commit your credentials.
- Built against the Share-a-Naan clone. Selectors and behaviour would differ on the real Instagram.

## License

MIT