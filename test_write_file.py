from functions.write_file import write_file


if __name__ == "__main__":

    print("Result for lorem.txt overwrite:")
    print(write_file(
        "calculator",
        "lorem.txt",
        "wait, this isn't lorem ipsum"
    ))
    print()

    print("Result for pkg/morelorem.txt creation:")
    print(write_file(
        "calculator",
        "pkg/morelorem.txt",
        "lorem ipsum dolor sit amet"
    ))
    print()

    print("Result for /tmp/temp.txt (should fail):")
    print(write_file(
        "calculator",
        "/tmp/temp.txt",
        "this should not be allowed"
    ))
    print()
