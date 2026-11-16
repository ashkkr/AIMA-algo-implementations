class ForwardBackward:
    # second-order markov rain/umbrella example:
    # - R_1 and R_2 are seeded independently from the prior 0.5/0.5, since the
    #   transition model needs two previous rain values before it applies
    # - P(R_t=True | R_{t-2}, R_{t-1}) is given by TRANSITION, for t >= 3
    # - P(U_t=True | R_t) is given by SENSOR
    PRIOR = {True: 0.5, False: 0.5}

    TRANSITION = {
        (True, True): 0.0,
        (True, False): 0.3,
        (False, True): 0.7,
        (False, False): 0.1,
    }

    SENSOR = {True: 0.9, False: 0.2}

    # because the transition depends on two previous rain values, the chain
    # is made first-order again by tracking the pair (R_{t-1}, R_t) as a
    # single augmented state
    STATES = [(a, b) for a in (True, False) for b in (True, False)]

    def _trans_prob(
        self, prev_state: tuple[bool, bool], curr_state: tuple[bool, bool]
    ) -> float:
        # curr_state's older value must equal prev_state's newer value
        if prev_state[1] != curr_state[0]:
            return 0.0
        p_true = self.TRANSITION[prev_state]
        return p_true if curr_state[1] else 1 - p_true

    def _sensor_prob_r(self, r: bool, u: bool) -> float:
        p_true = self.SENSOR[r]
        return p_true if u else 1 - p_true

    def _normalised(self, dist: dict) -> dict:
        total = sum(dist.values())
        return {k: v / total for k, v in dist.items()}

    def forward(self, evidence: list[bool]) -> list[dict[tuple[bool, bool], float]]:
        """f_2..f_T, f_t(Z_t) = P(Z_t | u_1:t), where Z_t = (R_{t-1}, R_t),
        normalised at every step. Z_2 = (R_1, R_2) is seeded straight from
        the prior; every later step multiplies in the previous-two-state
        transition."""
        messages = []
        f = {
            state: self.PRIOR[state[0]]
            * self.PRIOR[state[1]]
            * self._sensor_prob_r(state[0], evidence[0])
            * self._sensor_prob_r(state[1], evidence[1])
            for state in self.STATES
        }
        messages.append(self._normalised(f))

        for u in evidence[2:]:
            prev = messages[-1]
            f = {
                curr_state: sum(
                    prev[prev_state] * self._trans_prob(prev_state, curr_state)
                    for prev_state in self.STATES
                )
                * self._sensor_prob_r(curr_state[1], u)
                for curr_state in self.STATES
            }
            messages.append(self._normalised(f))
        return messages

    def backward(self, evidence: list[bool]) -> list[dict[tuple[bool, bool], float]]:
        """b_2..b_T, b_t(Z_t) = P(u_{t+1:T} | Z_t); b_T is all ones."""
        n = len(evidence) - 1  # number of Z states, Z_2..Z_T
        messages: list[dict] = [None] * n
        messages[n - 1] = {state: 1.0 for state in self.STATES}

        for i in range(n - 2, -1, -1):
            u_next = evidence[i + 2]
            b_next = messages[i + 1]
            messages[i] = {
                state: sum(
                    self._trans_prob(state, next_state)
                    * self._sensor_prob_r(next_state[1], u_next)
                    * b_next[next_state]
                    for next_state in self.STATES
                )
                for state in self.STATES
            }
        return messages

    def forward_backward(self, evidence: list[bool]) -> list[dict[bool, float]]:
        """Smoothed P(R_t=True | u_1:T) for t = 1..T."""
        forward_msgs = self.forward(evidence)
        backward_msgs = self.backward(evidence)

        # R_1's marginal only shows up as the first coordinate of Z_2
        joint_2 = self._normalised(
            {
                state: forward_msgs[0][state] * backward_msgs[0][state]
                for state in self.STATES
            }
        )
        r1_marginal = {True: 0.0, False: 0.0}
        for state, p in joint_2.items():
            r1_marginal[state[0]] += p

        smoothed = [r1_marginal]
        for f, b in zip(forward_msgs, backward_msgs):
            joint = self._normalised(
                {state: f[state] * b[state] for state in self.STATES}
            )
            marginal = {True: 0.0, False: 0.0}
            for state, p in joint.items():
                marginal[state[1]] += p
            smoothed.append(marginal)
        return smoothed

    def most_likely_sequence(self, evidence: list[bool]) -> list[bool]:
        """Per-timestep argmax of the smoothed marginals, R_1..R_T."""
        return [dist[True] >= dist[False] for dist in self.forward_backward(evidence)]

    def evidence_probability(self, evidence: list[bool]) -> float:
        """P(u_1:T), via an unnormalised forward pass."""
        state_prob = {
            state: self.PRIOR[state[0]]
            * self.PRIOR[state[1]]
            * self._sensor_prob_r(state[0], evidence[0])
            * self._sensor_prob_r(state[1], evidence[1])
            for state in self.STATES
        }
        for u in evidence[2:]:
            prev = state_prob
            state_prob = {
                curr_state: sum(
                    prev[prev_state] * self._trans_prob(prev_state, curr_state)
                    for prev_state in self.STATES
                )
                * self._sensor_prob_r(curr_state[1], u)
                for curr_state in self.STATES
            }
        return sum(state_prob.values())

    def sequence_probability(
        self, states: list[bool], evidence: list[bool]
    ) -> tuple[float, float]:
        """Joint P(R_1=states[0], ..., R_T=states[-1], u_1:T) and the
        corresponding posterior P(states | u_1:T), built by repeatedly
        multiplying each state's probability given its two predecessors
        (the first two states just use the prior, having no predecessors).
        """
        joint = self.PRIOR[states[0]] * self._sensor_prob_r(states[0], evidence[0])
        joint *= self.PRIOR[states[1]] * self._sensor_prob_r(states[1], evidence[1])

        for t in range(2, len(states)):
            p_true = self.TRANSITION[(states[t - 2], states[t - 1])]
            p_state = p_true if states[t] else 1 - p_true
            joint *= p_state * self._sensor_prob_r(states[t], evidence[t])

        posterior = joint / self.evidence_probability(evidence)
        return joint, posterior


if __name__ == "__main__":
    forwardBackward = ForwardBackward()
    evidence = [True, True, True, True, True, True, True, True, True]
    result = forwardBackward.forward_backward(evidence)
    for t, dist in enumerate(result, start=1):
        print(f"P(R_{t}=True | u_1:{len(evidence)}) = {dist[True]:.6f}")

    sequence = forwardBackward.most_likely_sequence(evidence)
    print("Most likely smoothed sequence:", sequence)

    joint_prob, posterior_prob = forwardBackward.sequence_probability(
        sequence, evidence
    )
    print(f"P(sequence, u_1:{len(evidence)}) = {joint_prob:.6e}")
    print(f"P(sequence | u_1:{len(evidence)}) = {posterior_prob:.6f}")
