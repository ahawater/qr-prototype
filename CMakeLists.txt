cmake_minimum_required(VERSION 3.10)
project(PybindExample)

# Manually set OpenCV path
set(OPENCV_DIR "/home/aly-hawater/git/opencv_install")

# Find pybind11 (ensure pybind11 is installed)
find_package(pybind11 REQUIRED)
find_package(Python REQUIRED)

# Add the executable
add_executable(main main.cpp)

include_directories(${Python_INCLUDE_DIRS})

# Link Python libraries to your target
target_link_libraries(main PRIVATE
    ${OPENCV_DIR}/install/lib/libopencv_core.so
    ${OPENCV_DIR}/install/lib/libopencv_imgproc.so
    ${OPENCV_DIR}/install/lib/libopencv_highgui.so
    ${OPENCV_DIR}/install/lib/libopencv_imgcodecs.so
    ${OPENCV_DIR}/install/lib/libopencv_objdetect.so
    ${Python_LIBRARIES}  # Link Python library
    pybind11::embed 
)


target_include_directories(main PRIVATE
    ${pybind11_INCLUDE_DIRS}  # Ensures pybind11 headers (including numpy) are found
    ${OPENCV_DIR}/install/include/opencv4 
)

