#include <pybind11/embed.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

namespace py = pybind11;

void processImageWithPython(const cv::Mat& inputImage) {
    py::scoped_interpreter guard{};  // Start Python interpreter

    // Convert cv::Mat to numpy array
    std::cout << "started python interpreter" << std::endl;

    py::module_ np = py::module_::import("numpy");

    std::cout << "imported numpy" << std::endl;

    py::module_ cv2 = py::module_::import("cv2");

    std::cout << "imported cv2" << std::endl;

    auto img = py::array_t<unsigned char>(
        {inputImage.rows, inputImage.cols, inputImage.channels()},
        inputImage.data
    );

    std::cout << "converted cv::Mat to numpy array" << std::endl;

    // Import the Python script 'qrcodereader' which contains 'detect_qr'
    // Import the sys module to manipulate sys.path
    py::module_ sys = py::module_::import("sys");

    // Add the parent directory to the sys.path
    sys.attr("path").attr("append")("../");

    py::module_ script = py::module_::import("qrcodereader");

    std::cout << "imported qrcodereader" << std::endl;

    // Call the Python 'detect_qr' function
    py::object result = script.attr("detect_qr")(img);

    // Check if the result is a tuple (since detect_qr returns multiple values)
    if (py::isinstance<py::tuple>(result)) {
        // Cast the result to a tuple
        py::tuple result_tuple = result.cast<py::tuple>();

        // Extract each element from the tuple
        float u = result_tuple[0].cast<float>();         // Extract float
        std::string detected_code = result_tuple[1].cast<std::string>();  // Extract string
        bool error = result_tuple[2].cast<bool>();       // Extract bool

        // Now, you can use these values in your C++ code
        std::cout << "u: " << u << std::endl;
        std::cout << "Detected QR Code: " << detected_code << std::endl;
        std::cout << "Error: " << (error ? "True" : "False") << std::endl;

    } else {
        std::cerr << "Expected a tuple, but got a different type!" << std::endl;
    }

}

int main() {
    std::cout << "OpenCV version: " << CV_VERSION << std::endl;
    cv::Mat image = cv::imread("../data/v.12 lower camera crop.jpg");
    if (image.empty()) {
        std::cerr << "Error loading image" << std::endl;
        return -1;
    }
    std::cout << "Image size: " << image.size() << std::endl;

    // Process image with Python function
    processImageWithPython(image);

    return 0;
}
