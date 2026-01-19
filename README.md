## Take-Home Exercise: Live Data Monitor

You are given:

* `historical.csv` – a time-series dataset with columns:

  ```
  time, ch1
  ```
* `feed_generator.py` – a small script that replays `historical.csv` into a growing file (`live.csv`) to simulate a live data feed.

The generator overwrites `live.csv` at startup and then appends one row at a time.
It supports a single option to control playback speed:

```
--speed 1.0   # real-time
--speed 2.0   # 2x faster
--speed 4.0   # 4x faster
```

Example:

```
python feed_generator.py --input data/historical.csv --output data/live.csv --speed 1.0
```

Your task is to build a small standalone desktop application in Python that visualizes this live data.
The application will be used by a lab scientist to monitor and annotate a live experimental data feed.

### Requirements

Build a Python application that:

1. Watches `live.csv` as it grows and updates in near real-time.
2. Displays the data in a plot.
3. Shows some simple derived information for the current view, for example:

   * Latest value
   * Rolling mean over the last N samples (N can be fixed)
4. Includes a **Flag** feature:

   * A **"Flag"** button that marks a point of interest on the plot at the time the button is pressed (using the latest available data point).
   * The user must be able to enter a short **text description** for the flag (for example via a text box, dialog, or input field next to the button).
   * Flag markers should remain visible on the plot.
   * Flag data should be persisted (for example in `flags.csv`) containing at least:

     * time (or timestamp)
     * description
5. Remains responsive while updating (the UI should not freeze).

Guidance:

* Python is required.
* Using tkinter, pandas, and matplotlib is encouraged, but not mandatory.
* The UI can be simple and ugly. Clarity and correctness matter more than polish.
* You do not need to package this as an executable. It just needs to be easy for another developer to run.

### Deliverables

Please provide a *Private GitHub* repository containing:

* Your source code
* A short `README.md` explaining:

  * How to install dependencies
  * How to run your app
  * How flags are created and stored
  * Any design decisions you made
  * What you would improve with more time

* Your private repo should be shared with the owner of this repository, `mmcaw`

### Time Expectation

This exercise is designed to take around **2–3 hours**.
We are not looking for perfection. Feel free to use AI coding assistants. We are interested in:

* How you structure a small application
* How you handle real-time-ish data
* Code clarity and naming
* Thoughtfulness about the user
* Your ability to explain what you built
