// Standard Atmosphere Calculator.cpp
#include <iostream>
#include <cmath>

// Function to calculate the pressure with given values
double calculatePressure(const double& p_0, const double& T_0, const double& T_1, const double& a, const double& h_1, const double& h_0) {
    double p_1;
    if (a != 0) 
    {
        p_1 = p_0 * pow(T_1 / T_0, (-9.80665) / (a * 287)); 
    }
    else 
    {
        p_1 = p_0 * exp((-9.80665 * (h_1 - h_0) )/(287*T_0));
    }
    std::cout << "Lapse rate:         " << a << " (K*m^-1)\n";
    std::cout << "Altitude Change:    " << h_0 << " -> " << h_1 << " (m)\n";
    std::cout << "Temperature Change: " << T_0 - 273.15 << " -> " << T_1 - 273.15<< " (C)\n";
    std::cout << "Pressure Change:    " << p_0 << " -> " << p_1 << " (N*m^-2); Percentage of sea level: " << (p_1 * 100) / 101325 << " %\n";
    std::cout << "Density Change:     " << p_0 / (287 * T_0) << " -> " << p_1 / (287 * T_1) << " (kg*m^-3)\n\n";
    return p_1;
}

// The main juice
double calculateNextLayer(const double& maxAltitude, const double& p_0 = 101325, const double& h_0 = 0, const double& T_0 = 288.15, const int& iteration = 0) {
    // {Altitude, Lapse rate (Kelvin per meter) for below that altitude}
    double milePoints[8][2] = 
    { 
        {11000.0,   -0.0065},
        {20000.0,    0.0},
        {32000.0,    0.001},
        {47000.0,    0.0028},
        {51000.0,    0},
        {71000.0,   -0.0028},
        {84852.0,   -0.002},
        {10E304 ,    0} 
    };
    double a = milePoints[iteration][1];
    double h_1 = milePoints[iteration][0];
    double T_1 = T_0 + a * (h_1 - h_0);

    if (maxAltitude > milePoints[iteration][0]) 
    {
        double p_1 = calculatePressure(p_0, T_0, T_1, a, h_1, h_0);
        return calculateNextLayer(maxAltitude, p_1, h_1, T_1, iteration + 1);
    }
    else
    {
        return calculatePressure(p_0, T_0, T_1, a, maxAltitude, h_0);;
    }
}

int main()
{
    std::cout << "Standard Atmosphere Calculator made by Hugo Bruins, no copyright\n\n";
    long long keepGoing = 1;
    while (keepGoing != 0)
    {
        double inputAltitude;
        std::cout << "Type the altitude you want to calculate: \n";
        std::cin >> inputAltitude;
        std::cout << '\n';
        calculateNextLayer(inputAltitude);
        std::cout << "Do you want to calculate another Value?\n 1 for yes, 0 for no\n";
        std::cin >> keepGoing;
    }
    return 0;
}
