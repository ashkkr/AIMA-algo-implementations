from collections import deque

import numpy as np

# implementing this for a simple rain example, with a lag of 5 days
# here use the transition matrix of rain persists with prob 0.7
# umbrella is observed with 0.9 when r = true, and 0.2 when r = false
# rain prior is 0.5 and 0.5
# this is a first order markov process


class FixedLagSmoothing:
    """AIMA Fig. 14.6 FIXED-LAG-SMOOTHING for any discrete first-order HMM.

    prior:      length-n vector, P(X_0)
    transition: n x n matrix, T[i][j] = P(X_t = j | X_{t-1} = i)
    sensor:     dict mapping each evidence value e to the length-n vector
                P(e | X_t = i)
    lag:        d, how many steps behind the current time to smooth
    """

    def __init__(self, prior, transition, sensor, lag):
        self.T = np.asarray(transition, dtype=float)
        self.T_inv = np.linalg.inv(self.T)
        self.sensor = {e: np.asarray(p, dtype=float) for e, p in sensor.items()}
        self.lag = lag

        # persistent state of the algorithm
        self.t = 1
        self.f = np.asarray(prior, dtype=float)  # forward message f_{1:t-d}
        self.B = np.eye(len(self.f))  # backward transformation matrix
        self.evidence = deque()  # evidence window e_{t-d:t}

    def _O(self, e):
        """Observation matrix: diagonal of P(e | X_t = i)."""
        return np.diag(self.sensor[e])

    @staticmethod
    def _normalise(v):
        return v / v.sum()

    def _forward(self, f, e):
        """f_{1:t+1} = normalise(O_{t+1} T^T f_{1:t})."""
        return self._normalise(self._O(e) @ self.T.T @ f)

    def fixedLagSmoothing(self, e_t):
        """Feed in e_t; returns P(X_{t-d} | e_{1:t}), or None while t <= d."""
        self.evidence.append(e_t)
        O_t = self._O(e_t)

        if self.t > self.lag:
            # e_{t-d} leaves the window: fold it into the forward message
            e_old = self.evidence.popleft()
            self.f = self._forward(self.f, e_old)
            O_old_inv = np.diag(1.0 / self.sensor[e_old])  # O is diagonal
            self.B = O_old_inv @ self.T_inv @ self.B @ self.T @ O_t
        else:
            self.B = self.B @ self.T @ O_t

        self.t += 1
        if self.t > self.lag + 1:
            return self._normalise(self.f * (self.B @ np.ones(len(self.f))))
        return None


if __name__ == "__main__":
    # state index 0 = rain, 1 = no rain
    lag = 5
    smoother = FixedLagSmoothing(
        prior=[0.5, 0.5],
        transition=[[0.7, 0.3], [0.3, 0.7]],
        sensor={True: [0.9, 0.2], False: [0.1, 0.8]},
        lag=lag,
    )

    # umbrella observed on each of 15 days
    evidence = [
        True,
        True,
        False,
        True,
        True,
        True,
        False,
        False,
        True,
        True,
        False,
        True,
        True,
        True,
        False,
    ]

    for t, e in enumerate(evidence, start=1):
        result = smoother.fixedLagSmoothing(e)
        if result is None:
            print(f"day {t:2d}: umbrella={e!s:5}  not enough evidence yet")
        else:
            print(
                f"day {t:2d}: umbrella={e!s:5}  P(Rain_{t - lag}=True | u_1:{t}) = {result[0]:.6f}"
            )
