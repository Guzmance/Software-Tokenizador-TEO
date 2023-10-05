using System;

class Program
{
    static void Main()
    {
        int x = 10;
        float y = 3.14f;
        string hello = "Hello, World!";
        
        if (x > 5)
        {
            Console.WriteLine(hello);
        }
        else
        {
            Console.WriteLine("x is not greater than 5");
        }

        for (int i = 0; i < 5; i++)
        {
            Console.WriteLine("Iteration " + i);
        }

        // This is a single-line comment
        /* This is a
           multi-line comment /**/
    }
}
