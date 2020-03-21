from __init__ import *

# Start the program
if __name__ == "__main__":
    make_temp_dir()
    make_output_dir()
    program_ctrl()
    render.mainloop()
    make_temp_dir()  # Empty the temp dir