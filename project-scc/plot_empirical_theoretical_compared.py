import matplotlib.pyplot as plt
import math

# Run scc.py to populate the runtimes
from _runtimes import runtimes


def main():
    # Define this
    def theoretical_big_o(v, e):
        return 3 * (v * math.log(v) + e)

    # Fill in from result using compute_coefficient
    coeff = 4.821860837437274e-08

    vv = [v for _, _, v, _, _ in runtimes]
    ee = [e for _, _, _, e, _ in runtimes]

    predicted_runtime = [
        coeff * theoretical_big_o(v, e)
        for d, s, v, e, t in runtimes
    ]

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vv, ee, predicted_runtime, marker='o')

    # Plot theoretical fit
    ax.plot(
        vv,
        ee,
        predicted_runtime,
        c='k',
        ls=':',
        lw=2,
        alpha=0.5
    )

    # Update title, legend, and axis labels as needed
    ax.legend(['Observed', 'Empirical O(3(V log v + E))'])
    ax.set_xlabel('|V|')
    ax.set_ylabel('|E|')
    ax.set_zlabel('Runtime')
    ax.set_title('Time for SCC on Graph for Empirical')

    # You are welcome to play with the view angle as you'd like
    ax.view_init(elev=10, azim=-60)

    fig.show()
    fig.savefig('core_empirical_graph.svg')


if __name__ == '__main__':

    main()
