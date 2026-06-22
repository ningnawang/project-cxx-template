if(TARGET polyscope)
    return()
endif()

include(FetchContent)
FetchContent_Declare(
    polyscope
    GIT_REPOSITORY https://github.com/nmwsharp/polyscope.git
    GIT_TAG v2.4.0
)
FetchContent_MakeAvailable(polyscope)
