using System;

namespace SimpleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Введите текст:");
            string userInput = Console.ReadLine();

            Console.WriteLine("Вы ввели: " + userInput);
        }
    }
}
