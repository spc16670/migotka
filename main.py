import dao

import ania.boxplots.patients as p_plots
import ania.boxplots.carers as c_plots


def main():
    #dao.print_patients()
    c_plots.nasa_last_training_and_independent()
    #c_plots.nasa_first_last_training()
    #carers = load_carers()
    #print("\n----------------------\n" + str(carers))


if __name__ == "__main__":
    main()
