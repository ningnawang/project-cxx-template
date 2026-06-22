#include <iostream>

// libigl
#include <Eigen/Core>

// Polyscope
#include <polyscope/polyscope.h>
#include <polyscope/point_cloud.h>

int main(int argc, char* argv[])
{
    // ---------- Hello world ----------
    std::cout << "Hello, world!" << std::endl;

    // ---------- Polyscope ----------
    polyscope::init();

    // Register a simple point cloud so the viewer has something to show.
    Eigen::MatrixXd points(4, 3);
    points << 0.0, 0.0, 0.0,
              1.0, 0.0, 0.0,
              0.0, 1.0, 0.0,
              0.0, 0.0, 1.0;
    polyscope::registerPointCloud("hello points", points);

    // Launch the Polyscope GUI.
    polyscope::show();

    return 0;
}
